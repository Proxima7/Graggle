FROM python:3.10.8
ARG DEBIAN_FRONTEND=noninteractive

# Linux Dependencies
RUN apt update && apt upgrade -y && apt-get install ffmpeg libsm6 libxext6 -y && apt clean

COPY pip.ini /etc/pip.conf

# python requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir



#COPY ./database_accessor-4.3.7-py3-none-any.whl .
#RUN pip3 install ./database_accessor-4.3.7-py3-none-any.whl


COPY . .

# fasapi webservice
CMD python3 main.py