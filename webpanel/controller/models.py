# -*- coding: utf-8 -*-
from django.db import models

class Statuse(models.Model):
    """ Contains statuses which can be matched to hosts. """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "statuses"
        verbose_name = "status"


class Host(models.Model):
    """ Contains hosts with all parameters. """
    dns_name = models.CharField(max_length=64, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', unique=True)
    description = models.TextField()
    status = models.ForeignKey(Statuse, on_delete=models.CASCADE, null=True)
    last_seen = models.DateTimeField(null=True)
    synchronization_period = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "hosts"
        verbose_name = "host"

    def __str__(self):
        return str(self.dns_name)

class Group(models.Model):
    """ Contains logical groups. """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    members = models.ManyToManyField(Host, through='Membership')  # this shows through which table the Group is connected to the Host.

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "groups"
        verbose_name = "group"


class Membership(models.Model):
    """ Joins two tables: Hosts and Groups. """
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
        verbose_name_plural = "hosts <-> groups"
        verbose_name = "host <-> groups"


class Module(models.Model):
    """ Contains module with all paremeters. 
            Columns:
                - configuration: JSON
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    configuration = models.TextField()  # JSON

    class Meta:
        verbose_name_plural = "module"
        verbose_name = "module"


class Task(models.Model):
    """ Queue of tasks for hosts. """
    name = models.CharField(max_length=64, unique=True, db_index=True)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False)
    worker = models.ForeignKey(Host, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = "tasks"
        verbose_name = "task"
