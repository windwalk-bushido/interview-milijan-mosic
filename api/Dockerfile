# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /api/container
COPY requirements.txt /api/container
COPY app.py /api/container
COPY db.json /api/container
COPY gunicorn.conf.py /api/container

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
