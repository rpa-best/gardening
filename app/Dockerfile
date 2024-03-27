FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update
RUN apt-get -y install libev-dev libnss3 locales-all gdal-bin libpq5 libgdal-dev python3-gdal binutils libproj-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/