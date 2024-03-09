#FROM ubuntu:20.04
FROM python:3.8-slim


RUN apt-get update
RUN apt-get install -y python3-pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=infoscreen.py
ENV PYTHONPATH=/home/churchtools_infoscreen

RUN mkdir /home/churchtools_infoscreen
WORKDIR /home/churchtools_infoscreen