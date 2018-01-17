from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from datetime import timedelta

from controller.models import Host, HostStatus

@api_view(['GET', ])
def refresh_hosts_status(request):
    all_hosts = Host.objects.all()
    lost_status = HostStatus.objects.get(name="Lost")
    now = timezone.now()
    for h in all_hosts:
        if not h.last_seen:
            continue
        elif (now - timedelta(minutes=h.synchronization_period)) > h.last_seen:
            h.status = lost_status
            h.save()
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
