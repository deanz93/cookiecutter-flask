# Use an official Python runtime as a base image
FROM python:{{ cookiecutter.python_version }}-slim

RUN apt-get update -y && apt-get install curl wget unzip gnupg2 locales -y

RUN apt-get update -y

RUN apt install -y --allow-downgrades build-essential python3-gdal \
        libxml2 libxml2-dev gettext libmemcached-dev zlib1g-dev \
        libxslt1-dev libjpeg-dev libpng-dev libpq-dev \
        software-properties-common build-essential \
        git unzip gcc zlib1g-dev libgeos-dev libproj-dev

RUN sed -i -e 's/# C.UTF-8 UTF-8/C.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for GeoPandas and Python libraries
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-dev

# Copy the application code to the working directory
COPY . .

# Install dependencies
RUN cd /app && pip install --no-cache-dir -r requirements/local.txt

RUN pip install pygdal=="`gdal-config --version`.*"

# Expose the port the app runs on
EXPOSE 5000

# Set the entry point to start the application
CMD ["python", "run.py"]
