FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir 

COPY . .

COPY docs/ /app/docs/

CMD gunicorn --bind 0.0.0.0:9000 foodgram.wsgi:application
