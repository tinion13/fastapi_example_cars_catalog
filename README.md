# Cars Catalog

Тестовый backend-проект на **FastAPI** с использованием **асинхронной работы с БД** через **SQLAlchemy** и **aiosqlite**.


## Что реализовано

- REST API на FastAPI
- асинхронная работа с базой данных
- SQLAlchemy ORM
- SQLite в качестве базы данных
- авторизация и связанные зависимости
- разделение логики по слоям:
  - `routers` — маршруты API
  - `services` — бизнес-логика
  - `db` — модели и сессии
  - `dependencies` — зависимости FastAPI
  - `utils` — вспомогательные функции

## Стек

- **Python3.12**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **aiosqlite**
- **Pydantic**
- **Uvicorn**

