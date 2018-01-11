# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

import hashlib

class HostStatus(models.Model):
    """ Contains statuses which can be matched to host """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "host statuses"
        verbose_name = "host status"


class Host(models.Model):
    """ Contains host with all parameters """
    token = models.CharField(max_length=64, unique=True, db_index=True)
    dns_name = models.CharField(max_length=64, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', unique=True)
    description = models.TextField()
    status = models.ForeignKey(HostStatus, on_delete=models.CASCADE, null=True)
    last_seen = models.DateTimeField(null=True)
    synchronization_period = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.dns_name)

    def save(self, *args, **kwargs):
        if not self.token:  # run only once - while create
            self.token = hashlib.md5(self.dns_name.encode() + str(timezone.now()).encode()).hexdigest()
        super(Host, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "hosts"
        verbose_name = "host"

class Group(models.Model):
    """ Contains logical group """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    members = models.ManyToManyField(Host, through='Membership')  # this shows through which table the Group is connected to the Host.

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "groups"
        verbose_name = "group"


class Membership(models.Model):
    """ Joins two tables: Hosts and Groups """
    host = models.ForeignKey(Host, on_delete=models.CASCADE, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.host) + " <-> " + str(self.group)

    @staticmethod
    def bulk_save_host(host_obj, groups_name):
        Membership.objects.filter(host=host_obj).delete()  # remove all assignments
        for g in groups_name:
            group_obj = Group.objects.filter(name=g)
            if group_obj:
                # group_obj[0] => [0] becaouse group_obj is queryset with one object
                Membership.objects.create(host=host_obj, group=group_obj[0])
        return host_obj

    @staticmethod
    def bulk_save_group(hosts_name, group_obj):
        Membership.objects.filter(group=group_obj).delete()  # remove all assignments
        for h in hosts_name:
            host = Host.objects.filter(dns_name=h)
            if host:
                # host[0] => [0] becaouse host is queryset with one object
                Membership.objects.create(host=host[0], group=group_obj)
        return group_obj

    class Meta:
        verbose_name_plural = "memberships"
        verbose_name = "membership"


class Module(models.Model):
    """ Contains module with all paremeters
            Columns:
                - configuration: JSON
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    configuration = models.TextField()  # JSON

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "modules"
        verbose_name = "module"

class TaskStatus(models.Model):
    """ Contains statuses which can be matched to task """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "task statuses"
        verbose_name = "task status"


class Task(models.Model):
    """ Queue of tasks for hosts """
    name = models.CharField(max_length=64, db_index=True)
    description = models.TextField(null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False)
    worker = models.ForeignKey(Host, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, null=True)
    results = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    parameters = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def bulk_save(name, description, module, workers, enumeration=False):
        status = TaskStatus.objects.get(name="in queue")
        for i, w in enumerate(workers):
            number_of_workers = len(workers)
            worker = Host.objects.filter(dns_name=w)
            if worker:
                if not name:
                    name = module.name  # if name is empty, module name will be set
                # worker[0] => [0] becaouse host is queryset with one object
                if enumeration:
                    params = '{"local_id": %s, "number_of_workers": %s}' % (i, number_of_workers)
                    Task.objects.create(name=name, description=description, module=module, worker=worker[0],
                                        status=status, parameters=params)
                else:
                    Task.objects.create(name=name, description=description, module=module, worker=worker[0],
                                        status=status)
        return True

    class Meta:
        verbose_name_plural = "tasks"
        verbose_name = "task"
