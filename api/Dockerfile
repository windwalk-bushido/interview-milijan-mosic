# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /api/container
COPY requirements.txt /api/container
COPY gunicorn.conf.py /api/container
COPY app.py /api/container
COPY db.json /api/container

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
