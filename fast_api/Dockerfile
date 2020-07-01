# Start with a large python base image that includes gcc and other libraries
FROM python:3 as python-base
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN wget -O /usr/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64
RUN chmod +x /usr/bin/dumb-init

COPY main.py main.py

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Run our app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
