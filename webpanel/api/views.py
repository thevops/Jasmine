from django.shortcuts import render
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import logging
import json

from controller.models import Host, Task, TaskStatus, Module, HostStatus
from .serializers import TaskSerializer, ModuleSerializer

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
# create a file handler
handler = logging.FileHandler('api_views.log')
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s %(name)s.%(funcName)s.%(lineno)d: %(levelname)s %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


def authenticate(request):
    # check if host with given token exists
    try:
        token = request.POST['token']  # if not exists return None
    except Exception as e:
        print("Authorization " + str(e))
        return None

    host = Host.objects.filter(token=token).first()  # filter() -> if not exists returns empty list -> []
    return host

@api_view(['POST', ])
def list_of_waiting_tasks(request):
    """
    :param request: {"token": ...}
    :return: list of tasks to do
    """
    host = authenticate(request)
    if not host:
        return Response({"status": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    stat = TaskStatus.objects.get(name="in queue")
    tasks = Task.objects.filter(worker=host, status=stat)  # list of tasks with status 'in queue'
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', ])
def get_task(request, task_id=None):
    """
    :param request: {"token": ...}
    :param task_id:
    :return: task
    """
    host = authenticate(request)
    if not host:
        return Response({"status": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    if not task_id:
        return Response({"status": "task_id not found"}, status=status.HTTP_400_BAD_REQUEST)

    task = Task.objects.filter(id=task_id).first()
    if task and task.worker == host:
        stat = TaskStatus.objects.filter(name="in progress").first()
        task.status = stat
        task.save()
        serializer = TaskSerializer(task)
        logger.info("GET %s - %s -> %s" % (task.name, task.worker, task.module))
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"status": "task not exists or you are not owner of it"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def set_task_result(request, task_id=None):
    """
    :param request: {"token": ..., "status": ..., "results": <string>}
    :param task_id:
    :return: success or error
    """
    host = authenticate(request)
    if not host:
        return Response({"status": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    if not task_id:
        return Response({"status": "task_id not found"}, status=status.HTTP_400_BAD_REQUEST)

    status_ = request.POST.get("status")
    if not status_:
        return Response({"status": "status not found"}, status=status.HTTP_400_BAD_REQUEST)

    results = request.POST.get("results")
    if not results:
        return Response({"status": "results not found"}, status=status.HTTP_400_BAD_REQUEST)

    task = Task.objects.filter(id=task_id).first()
    if task and task.worker == host:
        stat = TaskStatus.objects.filter(name=status_).first()
        task.status = stat
        task.results = results
        task.save()
        # here we can send notification about completed task TODO
        logger.info("SET %s - %s -> %s" % (task.name, task.worker, task.module))
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "task not exists or you are not owner of it"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def get_module(request, module_id=None):
    """
    :param request: {"token": ...}
    :param module_id: 
    :return: module
    """
    host = authenticate(request)
    if not host:
        return Response({"status": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    if not module_id:
        return Response({"status": "task_id not found"}, status=status.HTTP_400_BAD_REQUEST)

    module = Module.objects.filter(id=module_id).first()
    if module:
        serializer = ModuleSerializer(module)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"status": "module not exists"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def get_configurations(request):
    """
    :param request: {"token": ...}
    :return: module
    """
    host = authenticate(request)
    if not host:
        return Response({"status": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    data = {
        "synchronization_period": host.synchronization_period
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST', ])
def periodic_report(request):
    """
    :param request: {"token": ...}
    :return: 
    """
    host = authenticate(request)
    if not host:
        return Response({"status": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    host_stat = HostStatus.objects.get(name="Active")
    host.last_seen = timezone.now()
    host.status = host_stat
    host.save()
    return Response(status=status.HTTP_200_OK)
