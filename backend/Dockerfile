FROM python:3.11-slim

RUN apt-get update 

RUN apt-get install -y gettext

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY foodgram_backend/ /app

CMD ["gunicorn", "foodgram_backend.wsgi:application", "--bind", "0:8000" ]