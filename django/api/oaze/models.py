from django.db import models
from django.utils import timezone

from dasktasks.models import DaskTask


class CsvDocument(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    # Files are immutable as we will have tasks that depend on them
    file = models.FileField(upload_to='documents/')


class SumAmountEuroTask(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey(DaskTask, on_delete=models.CASCADE)
    csv_document = models.OneToOneField(CsvDocument, on_delete=models.CASCADE)

    def get_task_result(self):
        pass

