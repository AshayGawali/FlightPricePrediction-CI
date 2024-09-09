FROM python:3.9.18-slim-bullseye

WORKDIR  /flight_env

COPY flight_env .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD python application.py
