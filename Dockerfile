FROM python:3.7.0-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y binutils libproj-dev gdal-bin libgdal-dev

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt --no-cache-dir

RUN useradd provider_service
RUN chown -R provider_service /app
USER provider_service
COPY . /app
RUN ./manage.py collectstatic --no-input