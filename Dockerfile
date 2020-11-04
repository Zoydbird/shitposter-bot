FROM python:3

ADD . /bot
WORKDIR /bot

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot.py"]
