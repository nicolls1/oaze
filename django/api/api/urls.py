from django.urls import include
from django.urls import re_path
from rest_framework import routers

from dasktasks import views as dask_views
from oaze import views as oaze_views

router = routers.DefaultRouter()
router.register(r'tasks', dask_views.DaskTaskViewSet, basename='dasktask')
router.register(r'csv-documents', oaze_views.CsvDocumentViewSet, basename='csvdocument')

urlpatterns = [
    re_path('^', include(router.urls)),
]

