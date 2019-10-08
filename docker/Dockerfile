FROM python:3.6.0

COPY requirements-dev.txt /requirements-dev.txt
COPY . /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

EXPOSE 8000