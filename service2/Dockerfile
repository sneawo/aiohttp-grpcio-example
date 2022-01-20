FROM python:3.9.9-slim-bullseye
ENV PYTHONUNBUFFERED 1
ENV IN_DOCKER 1

COPY requirements.txt /requirements.txt

RUN pip3 install pip --upgrade \
    && pip3 install -r /requirements.txt

EXPOSE 8080

WORKDIR /app

ADD . /app

VOLUME /app

CMD python -m app.main
