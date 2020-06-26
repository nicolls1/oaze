from rest_framework import serializers

from dasktasks.models import DaskTask


class DaskTaskSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField(source='get_status', read_only=True)
    result = serializers.CharField(read_only=True)

    class Meta:
        model = DaskTask
        fields = ('url', 'task_key', 'status', 'result', 'start_time', 'end_time', 'duration_ms')
        read_only_fields = ('start_time', 'end_time', 'duration_ms')
