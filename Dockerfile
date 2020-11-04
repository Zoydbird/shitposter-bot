FROM python:3.8-slim-buster

WORKDIR /bot

ADD shitposter.py /bot
ADD bot.py /bot
ADD requirements.txt /bot
ADD .env /bot


RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot.py"]
