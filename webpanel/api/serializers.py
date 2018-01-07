from rest_framework import serializers

from controller.models import Task, Module

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','name','description','module','results', 'timestamp','parameters')

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id','name','description','configuration')