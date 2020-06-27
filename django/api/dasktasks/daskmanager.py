from django.core.mail import send_mail
import logging
import traceback

from dask.distributed import Client, Future
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
            self.client = Client(preload='daskworkerinit.py', n_workers=2, threads_per_worker=1, memory_limit='4GB')
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
            task.duration_ms = int((task.end_time-task.start_time).total_seconds()*1000)
            task.save()
        elif future.status == 'error':
            task.status = future.status
            task.result = traceback.extract_tb(future.traceback()) + [future.exception()]
            task.end_time = timezone.now()
            task.duration_ms = int((task.end_time-task.start_time).total_seconds()*1000)
            task.save()
        else:
            logger.error(f'Task completed with unhandled status: {future.status}')

        # send email that a task has finished, could be much more complex, just keeping it simple
        if future.status == 'finished':
            # The format requested, I would do a more generic message for all tasks by just passing task id and
            # a preview of the result, but if this is just a micro service for this particular task then it can work
            result = future.result()
            formatted_time = task.end_time.strftime("%d/%m/%Y %H:%M")
            message = f'{formatted_time} - {result["lines"]} entries processed, sum: {result["sum"]}'
        elif future.status == 'error':
            message = f'Task id {task.task_key} failed.'
        else:
            message = f'Task id {task.task_key} completed with unknown status: {future.status}'

        send_mail(
            'Task Completed',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.TASK_INFO_EMAIL],
            fail_silently=False,
        )

