from dask import delayed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dasktasks.daskmanager import DaskManager
from dasktasks.serializers import DaskTaskSerializer
from oaze.models import CsvDocument, SumAmountEuroTask
from oaze.serializers import CsvDocumentSerializer, SumAmountEuroTaskSerializer


class CsvDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CsvDocumentSerializer
    queryset = CsvDocument.objects.all()


class SumAmountEuroTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SumAmountEuroTaskSerializer
    queryset = SumAmountEuroTask.objects.all()

    @action(['post'], detail=False)
    def process_documents(self, request, pk=None):
        pass
        '''
        # Get objects from database
        numbers = list(Number.objects.all().values_list('value', flat=True))

        # Build graph
        squares = []
        for number in numbers:
            number_squared = delayed(lambda n: n**2)(number)
            squares.append(number_squared)
        sum_squares = delayed(sum)(squares)

        # Submit graph to Dask
        dask_task = DaskManager().compute(sum_squares)

        # Return task
        return Response(DaskTaskSerializer(instance=dask_task, context=self.get_serializer_context()).data)
        '''
