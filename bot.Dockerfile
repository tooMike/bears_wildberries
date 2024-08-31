FROM python:3.10

WORKDIR /bot

COPY bot_requirements.txt .

RUN pip install --no-cache-dir -r bot_requirements.txt

COPY ./bot /bot

CMD ["python", "main.py"]
