from rest_framework import serializers

from oaze.models import CsvDocument, SumAmountEuroTask


class CsvDocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CsvDocument
        fields = ('url', 'create_time', 'file')
        read_only_fields = ('create_time',)


class SumAmountEuroTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SumAmountEuroTask
        fields = ('url', 'create_time', 'task', 'csv_document')
        read_only_fields = ('create_time',)
