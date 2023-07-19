FROM python:3.10.0-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

# Install Redis and RabbitMQ dependencies
RUN apt-get update && apt-get install -y rabbitmq-server redis-server

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN mv /code/app/services/consume.py /code/
# RUN python consume.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
