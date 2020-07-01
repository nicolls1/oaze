from rest_framework import serializers

from oaze.models import CsvDocument


class CsvDocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CsvDocument
        fields = ('url', 'id', 'create_time', 'file', 'sum_task')
        read_only_fields = ('create_time', 'sum_task')

