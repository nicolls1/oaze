from unittest.mock import MagicMock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from graphs import graphs
from dasktasks.daskmanager import DaskManager
from dasktasks.models import DaskTask
from oaze.models import CsvDocument
from oaze import views


class CsvDocumentTests(APITestCase):
    csv_path = 'testfiles/1000.csv'

    def test_create(self):
        task = DaskTask(task_key='123')
        task.save()

        compute_mock = MagicMock()
        compute_mock.compute.return_value = task
        views.DaskManager = MagicMock(return_value=compute_mock)
        views.sum_csv_graph = MagicMock()
        url = reverse('csvdocument-list')
        with open(self.csv_path, 'rb') as image_data:
            data = {'file': image_data}
            response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_document = CsvDocument.objects.get(id=response.data['id'])
        views.sum_csv_graph.assert_called_with(new_document.file.url)

    def test_create_no_file(self):
        url = reverse('csvdocument-list')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
