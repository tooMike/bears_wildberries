FROM python:3.10

WORKDIR /fastapi
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Копируем код приложения
COPY ./app /fastapi/app
COPY ./alembic /fastapi/alembic
COPY alembic.ini /fastapi/alembic.ini

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
