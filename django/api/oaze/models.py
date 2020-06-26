from django.db import models
from django.utils import timezone

from dasktasks.models import DaskTask


class CsvDocument(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='documents/')
    sum_task = models.ForeignKey(DaskTask, on_delete=models.CASCADE, null=True)

