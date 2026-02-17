FROM python:3.11-slim

WORKDIR /tg-bot

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app/lil_gnida/main.py"]