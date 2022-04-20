FROM python:3.7-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/stream-pj-32067718f958.json"

CMD ["python", "streaming.py"]