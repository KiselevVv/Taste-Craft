# Foodgram
[![.github/workflows/foodgram_workflow.yml](https://github.com/KiselevVv/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/KiselevVv/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## Описание

Сервис, в котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Также у пользователей есть возможность создавать список продуктов, которые нужно купить для приготовления выбранных блюд, и загружать его в формате PDF.

В рамках учебного проекта был разработан backend сервиса и настроен CI/CD.

## Доступ

Проект запущен на сервере и доступен по адресам:
- http://158.160.61.158/recipes
- Админ-зона: http://158.160.61.158/admin/
- API: http://158.160.61.158/api/
 
## Стек технологий
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Github Actions

## Зависимости
- Перечислены в файле backend/requirements.txt

## Для запуска на собственном сервере:
1. Скопируйте из репозитория файлы, расположенные в директории infra:
    - docker-compose.yml
    - nginx.conf
2. На сервере файлы docker-compose.yml и пустой .env поместите в домашней директории;
3. Файл nginx.conf должен находится в директории nginx;
4. Локальный файл .env должен быть заполнен следующими данными:
```
SECRET_KEY=<КЛЮЧ>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<ИМЯ БАЗЫ ДАННЫХ>
POSTGRES_USER=<ИМЯ ЮЗЕРА БД>
POSTGRES_PASSWORD=<ПАРОЛЬ БД>
DB_HOST=db
DB_PORT=5432
```

5. В домашней директории следует выполнить команды:
```
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```

6. Для создания суперпользователя, выполните команду:
```
docker-compose exec backend python manage.py createsuperuser
```

7. Для добавления ингредиентов в базу данных, выполните команду:
```
docker-compose exec backend python manage.py load_ingredients
```
После выполнения этих действий проект будет запущен в трех контейнерах (backend, db, nginx) и доступен по адресам:

- Главная страница: http://<ip-адрес>/recipes/
- API проекта: http://<ip-адрес>/api/
- Admin-зона: http://<ip-адрес>/admin/
8. Теги вручную добавляются в админ-зоне в модель Tags;
9. Проект запущен и готов к регистрации пользователей и добавлению рецептов.

### Автор
Киселев Влад
