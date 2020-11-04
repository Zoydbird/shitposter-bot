FROM python:3.8-slim-buster

ADD . /bot
WORKDIR /bot

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot.py"]
