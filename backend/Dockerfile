FROM python:3.10.8
ARG DEBIAN_FRONTEND=noninteractive

# Linux Dependencies
RUN apt update && apt upgrade -y && apt-get install ffmpeg libsm6 libxext6 -y && apt clean

# manual database_accessor
ARG DATABASE_ACCESSOR_VERSION=1.6.9
COPY whl/database_accessor-$DATABASE_ACCESSOR_VERSION-py3-none-any.whl database_accessor-$DATABASE_ACCESSOR_VERSION-py3-none-any.whl
RUN pip3 install ./database_accessor-$DATABASE_ACCESSOR_VERSION-py3-none-any.whl

# python requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .

# fasapi webservice
CMD python3 main.py