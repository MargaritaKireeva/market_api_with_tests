# Market API

REST API для маркетплейса на **FastAPI** с PostgreSQL и JWT-аутентификацией.

## Технологии

- Python 3.12, FastAPI, Pydantic v2
- PostgreSQL, psycopg2-binary
- JWT (PyJWT), bcrypt (passlib)
- Docker, docker-compose
- pytest, requests

## Запуск через Docker

```bash
docker-compose up --build
```

Сервер будет доступен на `http://localhost:8000`.

Swagger-документация: `http://localhost:8000/docs`

## Переменные окружения (`.env`)

| Переменная   | Описание             |
| ------------ | -------------------- |
| SECRET_KEY   | Секретный ключ JWT   |
| DB_HOST      | Хост БД              |
| DB_NAME      | Имя БД               |
| DB_USER      | Пользователь БД      |
| DB_PASS      | Пароль БД            |

## Структура проекта

```
├── app/
│   ├── api/v1/routes/   # Эндпоинты (auth, products, cart, orders)
│   ├── core/            # Подключение к БД, JWT-логика
│   ├── db/              # SQL-инициализация
│   ├── models/          # Pydantic-схемы
│   └── main.py          # Точка входа
├── tests/               # pytest-тесты
├── Dockerfile
└── docker-compose.yml
```

## Аутентификация

Эндпоинты корзины и заказов требуют JWT-токен. Токен передаётся в заголовке:

```
Authorization: Bearer <token>
```

Токен живёт 7 дней.

---

## API Endpoints

### Auth

#### `POST /auth/register` — Регистрация пользователя

**Request body:**
```json
{
  "email": "user@mail.com",
  "password": "secret123"
}
```

**`201` — Успех:**
```json
{
  "id": 1,
  "email": "user@mail.com"
}
```

**`409` — Пользователь уже существует:**
```json
{
  "detail": "User already exists"
}
```

---

#### `POST /auth/login` — Вход в систему

**Request body:**
```json
{
  "email": "user@mail.com",
  "password": "secret123"
}
```

**`200` — Успех:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**`401` — Неверные учётные данные:**
```json
{
  "detail": "Invalid credentials"
}
```

---

### Products

#### `GET /products` — Список всех товаров

**`200` — Успех:**
```json
[
  {
    "id": 1,
    "name": "iPhone 15",
    "price": 999.99
  }
]
```

---

#### `GET /products/{product_id}` — Получить товар по ID

**`200` — Успех:**
```json
{
  "id": 1,
  "name": "iPhone 15",
  "price": 999.99
}
```

**`404` — Товар не найден:**
```json
{
  "detail": "Product not found"
}
```

---

#### `POST /products` — Создать товар

**Request body:**
```json
{
  "name": "iPhone 15",
  "price": 999.99
}
```

**`201` — Успех:**
```json
{
  "id": 1,
  "name": "iPhone 15",
  "price": 999.99
}
```

---

#### `PATCH /products/{product_id}` — Обновить товар

**Request body (все поля опциональны):**
```json
{
  "name": "iPhone 15 Pro",
  "price": 1299.99
}
```

**`200` — Успех:**
```json
{
  "id": 1,
  "name": "iPhone 15 Pro",
  "price": 1299.99
}
```

**`404` — Товар не найден:**
```json
{
  "detail": "Product not found"
}
```

---

#### `DELETE /products/{product_id}` — Удалить товар

**`200` — Успех:**
```json
{
  "status": "deleted"
}
```

**`404` — Товар не найден:**
```json
{
  "detail": "Product not found"
}
```

---

### Cart (требуется токен)

#### `GET /cart` — Просмотр корзины

**`200` — Успех:**
```json
[
  {
    "product_id": 1,
    "quantity": 2
  }
]
```

**`404` — Корзина пуста:**
```json
{
  "detail": "Cart is empty"
}
```

---

#### `POST /cart/add` — Добавить товар в корзину

**Request body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

При повторном добавлении того же товара количество суммируется.

**`200` — Успех:**
```json
{
  "status": "added"
}
```

**`404` — Товар не найден:**
```json
{
  "detail": "Product not found"
}
```

---

#### `DELETE /cart/remove` — Очистить корзину

**`200` — Успех (тело ответа отсутствует)**

---

### Orders (требуется токен)

#### `POST /orders` — Создать заказ из корзины

Переносит все товары из корзины в заказ со статусом `created` и очищает корзину.

**`201` — Успех:**
```json
{
  "id": 1,
  "user_id": 1,
  "status": "created"
}
```

**`400` — Корзина пуста:**
```json
{
  "detail": "Cart is empty"
}
```

---

#### `GET /orders/{order_id}` — Получить заказ по ID

**`200` — Успех:**
```json
{
  "id": 1,
  "user_id": 1,
  "status": "created"
}
```

**`404` — Заказ не найден:**
```json
{
  "detail": "Order not found"
}
```

---

#### `PATCH /orders/{order_id}/status?status=confirmed` — Обновить статус заказа

Доступные статусы: `created`, `confirmed`, `shipped`, `delivered`, `cancelled`.

Правила переходов:
- `created` → `confirmed`, `cancelled`
- `confirmed` → `shipped`, `cancelled`
- `shipped` → `delivered`
- `delivered` → (финальный)
- `cancelled` → (финальный)

**`200` — Успех:**
```json
{
  "status": "updated"
}
```

**`404` — Заказ не найден:**
```json
{
  "detail": "Order not found"
}
```

**`422` — Недопустимый статус:**
```json
{
  "detail": "Invalid status. Allowed: ['created', 'confirmed', 'shipped', 'delivered', 'cancelled']"
}
```

---

#### `POST /orders/{order_id}/cancel` — Отменить заказ

**`200` — Успех:**
```json
{
  "status": "cancelled"
}
```

**`404` — Заказ не найден:**
```json
{
  "detail": "Order not found"
}
```

---

## Тесты

Перед запуском тестов должен быть запущен сервер (`http://localhost:8000`).

```bash
pytest tests -v
```
