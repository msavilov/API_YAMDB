
### api_yamdb

![githab](https://raw.githubusercontent.com/Zolibot/Interview_of_a_real_fighter/main/bender.gif)


![](https://img.shields.io/badge/license-MIT-green)
![](https://img.shields.io/badge/Powered%20by-Python3.9-green)


## Оглавление

- [Оглавление](#оглавление)
  - [Авторы](#авторы)
  - [Описание](#описание)
  - [Технологии](#технологии)
  - [Запуск проекта в dev-режиме](#запуск-проекта-в-dev-режиме)
  - [Загрузка тестовых данных в базу данных](#загрузка-тестовых-данных-в-базу-данных)
  - [Примеры API запросов](#примеры-api-запросов)
    - [Получение информации о произведении](#получение-информации-о-произведении)
    - [Получение отзыва по id](#получение-отзыва-по-id)

### Авторы

- [Максим Савилов - team leader](https://github.com/msavilov/)
- [Юлия Мелик-Гусейнова - developer](https://github.com/JuliaM-G)
- [Александр Андреевич - developer](https://github.com/Zolibot)

### Описание

Проект YaMDb собирает отзывы пользователей на различные произведения.
Пользователи могут оставлять отзывы и выставлять оценки произведениям из 
различных категорий. К этим отзывам есть возможность оставлять комментарии.
Из пользовательских оценок формируется усреднённым оценка произведения.
Аутенфикация пользователей происходит по JWT.

### Технологии

- ![](https://img.shields.io/badge/Python-3.9-brightgreen)

- ![](https://img.shields.io/badge/Django-3.2-brightgreen)

- ![](https://img.shields.io/badge/djangorestframework-3.12.4-brightgreen)

### Запуск проекта в dev-режиме

- клонировать репозиторий или скачать архив

```bash
git clone https://github.com/msavilov/api_yamdb.git
```

- Установите и активируйте виртуальное окружение

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

- обновить pip

```bash
python3 -m pip install --upgrade pip
```

- Установите зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

- В папке с файлом manage.py выполните команду:

```bash
python3 manage.py runserver
```

- документация к API ``http://127.0.0.1:8000/redoc/``

### Загрузка тестовых данных в базу данных

- Запуск миграций
```bash
python3 manage.py migrate
```
- Импорт данных из CSV файлов в БД
```bash
python3 manage.py load_db_from_csv
```

### Примеры API запросов

#### Получение информации о произведении
- Права доступа: Доступно без токена
- Запрос: GET /titles/{titles_id}/
- Статус ответа: 200 Удачное выполнение запроса
Ответ:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

#### Получение отзыва по id
- Права доступа: Доступно без токена
- Запрос: GET /titles/{title_id}/reviews/{review_id}/
- Статус ответа: 200 Удачное выполнение запроса
- Ответ:
  
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
