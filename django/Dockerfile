FROM python:3 as python-base
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN wget -O /usr/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64
RUN chmod +x /usr/bin/dumb-init

COPY ./api /api
WORKDIR /api

RUN python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Run our app
CMD ["gunicorn", "-b", ":8000", "api.wsgi"]
