import logging
import traceback

from dask.distributed import Client, LocalCluster, Future
from django.conf import settings
from django.utils import timezone

from dasktasks.models import DaskTask

logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DaskManager(metaclass=Singleton):
    def __init__(self):
        if settings.DASK_SCHEDULER_HOST is None:
            self.client = Client(preload='daskworkerinit.py', n_workers=2, threads_per_worker=1, memory_limit='1GB')
        else:
            self.client = Client(settings.DASK_SCHEDULER_HOST+':'+settings.DASK_SCHEDULER_PORT)

    def compute(self, graph):
        future = self.client.compute(graph)
        future.add_done_callback(self.task_complete)
        dask_task = DaskTask.objects.create(task_key=future.key)
        return dask_task

    def get_future_status(self, task_key):
        return Future(key=task_key, client=self.client).status

    @staticmethod
    def task_complete(future):
        task = DaskTask.objects.get(pk=future.key)

        if future.status == 'finished':
            task.status = future.status
            task.result = future.result()
            task.end_time = timezone.now()
            task.duration = int((task.end_time-task.start_time).total_seconds()*1000)
            task.save()
        elif future.status == 'error':
            task.status = future.status
            task.result = traceback.extract_tb(future.traceback()) + [future.exception()]
            task.end_time = timezone.now()
            task.duration = int((task.end_time-task.start_time).total_seconds()*1000)
            task.save()
            # will cause exception to be thrown here
            future.result()
        else:
            logger.error('Task completed with unhandled status: ' + future.status)
