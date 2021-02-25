FROM python:3.9-buster

COPY main.py /app/main.py
COPY Pipfile.lock /app/Pipfile.lock
COPY src /app/src

WORKDIR /app

RUN pip3 install pipenv
RUN pipenv install --system
ENTRYPOINT ["python3", "main.py"]
