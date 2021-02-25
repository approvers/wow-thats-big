FROM python:3.9-buster

COPY main.py /app/main.py
COPY src /app/src

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
