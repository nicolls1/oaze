from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from dasktasks.daskmanager import DaskManager
from graphs.graphs import sum_csv_graph
from oaze.models import CsvDocument
from oaze.serializers import CsvDocumentSerializer


class CsvDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CsvDocumentSerializer
    queryset = CsvDocument.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_document = serializer.save()

        graph = sum_csv_graph(serializer.data['file'])
        dask_task = DaskManager().compute(graph)
        csv_document.sum_task = dask_task
        csv_document.save()

        response_serializers = self.get_serializer(csv_document)

        headers = self.get_success_headers(serializer.data)
        return Response(response_serializers.data, status=status.HTTP_201_CREATED, headers=headers)
