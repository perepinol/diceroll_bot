FROM python:latest

WORKDIR /
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY diceroll_bot.py ./

CMD ["python", "diceroll_bot.py"]