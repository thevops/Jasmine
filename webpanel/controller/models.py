# -*- coding: utf-8 -*-
from django.db import models

class Statuses(models.Model):
    """ Contains statuses which can be matched to hosts. """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "statuses"
        verbose_name = "status"

class Hosts(models.Model):
    """ Contains hosts with all parameters. """
    dns_name = models.CharField(max_length=64, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', unique=True)
    description = models.TextField()
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, null=True)
    last_seen = models.DateTimeField(null=True)
    synchronization_period = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "hosts"
        verbose_name = "host"

class Groups(models.Model):
    """ Contains logical groups. """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "groups"
        verbose_name = "group"

class Modules(models.Model):
    """ Contains modules with all paremeters. 
            Columns:
                - configuration: JSON
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    configuration = models.TextField()  # JSON

    class Meta:
        verbose_name_plural = "modules"
        verbose_name = "module"

class GroupAssignment(models.Model):
    """ Joins two tables: Hosts and Groups. """
    host_id = models.ForeignKey(Hosts, on_delete=models.CASCADE, null=False)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = "hosts <-> groups"
        verbose_name = "host <-> groups"

class Tasks(models.Model):
    """ Queue of tasks for hosts. """
    name = models.CharField(max_length=64, unique=True, db_index=True)
    description = models.TextField()
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=False)
    worker = models.ForeignKey(Hosts, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = "tasks"
        verbose_name = "task"
