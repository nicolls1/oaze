import datetime
import asyncio
import os

import pandas as pd
import dask.dataframe as dd
from dask.distributed import Client
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi_mail import FastMail
from pydantic import BaseSettings


class Settings(BaseSettings):
    task_status_email: str = os.environ.get('TASK_STATUS_EMAIL', 'tasks@oaze.com')
    # You will have to setup an app password for your gmail to work
    # https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor
    # Could also just use a paid service like mailgun which is described in the other solution, just wanted to try
    # something different
    admin_email: str = os.environ.get('ADMIN_EMAIL', None)
    admin_email_password: str = os.environ.get('ADMIN_EMAIL_PASSWORD', None)


settings = Settings()
app = FastAPI()
client = Client(n_workers=2, threads_per_worker=1, memory_limit='4GB')


def send_email(destination, subject, body):
    if settings.admin_email is not None and settings.admin_email_password:
        mail = FastMail(email=settings.admin_email, password=settings.admin_email_password, tls=True, port="587",
                        service="gmail")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            mail.send_message(recipient=destination, subject=subject, body=body, text_format="plain")
        )
    else:
        print('Email not configured, tried sending:')
        print(f'Header: {subject}')
        print(f'Body: {body}')


def sum_csv(upload_file: UploadFile):
    file_data = pd.read_csv(upload_file.file)
    df = dd.from_pandas(file_data, npartitions=20)

    csv_sum = '{:.2f}'.format(df['amount EUR'].sum().compute())
    lines = df.shape[0].compute()

    formatted_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    message = f'{formatted_time} - {lines} entries processed, sum: {csv_sum}'
    send_email(settings.task_status_email, 'Task Finished', message)


@app.post("/sum_csv")
async def root(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    background_tasks.add_task(sum_csv, file)
    return {"message": "Processing."}
