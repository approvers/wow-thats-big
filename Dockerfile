FROM python:3.9-buster

COPY main.py /app/main.py
COPY src /app/src

WORKDIR /app
ENTRYPOINT ["python3", "main.py"]
