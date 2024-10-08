# Микросервис для получения и обработки данных о товарах с Wildberries

Данный проект представляет собой систему микросервисов для получения и обработки информации о товарах с сайта Wildberries. Система включает веб-сервис на основе FastAPI для обработки данных и телеграм-бот для взаимодействия с пользователями.

Проект запущен на удаленном сервере и готов к использованию. Настроен CI/CD с использованием GitHub Actions

Документация Swagger доступна по адресу: https://gazprom-id-6.ru/docs/

Очередь задач по обновлению информации о товарах доступна по адресу: https://flower.gazprom-id-6.ru/

Телеграм-бот доступен по адресу: https://t.me/Wildberries_Mike_bot

## Архитектура проекта

Микросервисы завернуты в Docker-контейнеры. Настроен Docker Compose для запуска всех сервисов, включая БД.

### 1. Микросервис по хранению и обработке данных о товаре

Основной микросервис построен на FastAPI и использует PostgreSQL для хранения информации о товарах. Данные обновляются каждые 5 минут с помощью Celery и Redis, который выступает брокером сообщений.

### 2. Телеграм-бот

Телеграм-бот, реализованный на Aiogram, позволяет пользователям вводить ID товара и получать актуальную информацию о его цене и доступности на складах.

## Реализация

### Микросервис по хранению и обработке данных о товаре.

Реализован микросервис по хранению и обработке данных о товарах с использованием фреймворка FastAPI,
а также PostgreSQL для хранения данных. 
В БД хранится следующая информация о товарах: 
- id товара (nm_id);
- цена товара;
- размеры товара;
- остатки товара на складах.

Если пользователь запрашивает информацию о товаре, которого нет в БД, происходит запрос этой информации с Wildberries (реализовано с использованием httpx).
Информация отдается пользователю, а в фоне данные записываются в БД (реализовано с использованием Background Tasks в FastAPI)

Настроено обновление информации о всех товарах в БД каждые 5 минут
(реализовано с использованием Celery beat, Redis используется в качестве брокера сообщений).

### Телеграм-бот

Реализован телеграм-бот с использованием Aiogram. Пользователь может ввести id товара и получить подробную информацию о нем.

Бот возвращает актуальные данные о цене, остатках товара на складах и общие остатки товара в удобном для чтения человеком формате.

Установлено ограничение количества запросов от одного пользователя: не более 1 запроса в минуту 
(реализовано с использованием механизма Throttling в Aiogram и Redis для хранения данных).


## Документация

Swagger документация доступна по адресу: [Swagger UI](https://gazprom-id-6.ru/docs)

Мониторинг очереди задач: [Flower Dashboard](https://flower.gazprom-id-6.ru/) (на данный момент доступно без аутентификации)

## Авторы проекта

[Beliaev Mikhail](https://github.com/tooMike) – [Telegram](https://t.me/gusoyn)

## Установка и запуск с Docker

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/tooMike/bears_wildberries
```

```
cd bears_wildberries
```

Запустить сборку проекта (для запуска необходимо добавить файл с секретами .env):

```
docker compose up
```

Проект будет доступен по адресу:

```
http://localhost:8000/
```

Flower будет доступен по адресу:

```
http://localhost:5555
```

## Спецификация

При локальном запуске документация будет доступна по адресу:

```
http://localhost:8000/docs/
```

## Стэк технологий:

- Python 3.10
- FastAPI 0.112
- Pydantic 2.8
- PostgreSQL 14
- SQLAlchemy 2.0
- Alembic 1.13
- Aiogram 2.25
- Docker, Docker Compose
- Celery, Flower

## Примеры запросов к API

### Получение информации о товаре

* Описание метода: получение информации о товаре.
* Права доступа: Доступно всем пользователям.
* Тип запроса: `GET`
* Эндпоинт: `/product/{nm_id}`

Пример успешного ответа:

```
{
  "nm_id": 0,
  "current_price": 0,
  "sum_quantity": 0,
  "quantity_by_sizes": [
    {
      "size": "string",
      "quantity_by_wh": [
        {
          "wh": 0,
          "quantity": 0
        }
      ]
    }
  ]
}
```

## Планы развития проекта

1. Добавить в информацию о товаре ссылку на фото товара.
2. Покрыть проект тестами