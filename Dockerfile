FROM python:3.8.5-slim-buster
RUN pip install --upgrade pip
# RUN apt-get update && apt-get install -y python-opencv libopencv-dev git
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
