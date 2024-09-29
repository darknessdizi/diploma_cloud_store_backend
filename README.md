Дипломная работа для fullstack-разработчика - облачное хранилище
===

## Backend

*Ссылка на git-hub репозиторий (backend):* https://github.com/darknessdizi/cloud-store-backend.git


## Последовательность установки
1. устанавливаем python
1. создали папку для проекта
1. создали файл .gitignore
1. создали гит репозиторий (**git init**)
1. создали виртуальное окружение (**python -m venv venv** или так py -3.10 -m venv venv)
1. в командной строке cmd *активировали виртуальное окружение* (venv\Scripts\activate.bat )
1. устанавливаем библиотеки для python:
    - pip install psycopg2-binary (для примера)
    - **pip install django**
    - pip install django-cors-headers (для CORS)
1. создаем файл requirements.txt командой в cmd терминале (**pip freeze > requirements.txt**) 
1. создали django проект (**django-admin startproject project_cloud_storage**)
1. устанавливаем *postgresql*:
    - запускаем установочный пакет postgresql-15.0-1-windows-x64.exe
    - зарегистрировать psql в переменных средах windows
    - проверяем что служба postgresql запущена
    - создаем базу данных например с именем test
1. устанавливаем *dbeaver* для графического отображения базы данных:
    - запускаем установочный пакет dbeaver-ce-22.2.2-x86_64-setup.exe
    - при запуске программы устанавливаем соединение с нашей базой test:
        1. указать имя базы данных test
        1. указать имя суперпользователя и пароль
        1. нажать тест соединения (при первой установке будет запрос скачать драйвера для postgresql)
        1. при успешном тестировании соединения нажать готово и базаданных будет отображена
1. заходим в папку project_cloud_storage (в командной строке **cd project_cloud_storage/**) и создаем приложение (**python manage.py startapp app_cloud_storage**)
    - приложение подключаем в файле settings.py:
    ```
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'app_cloud_storage',
        ]
    ```
    - в файле settings.py подключаем базу данных в джанго:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test',
            'USER': 'postgres',
            'PASSWORD': '12345678',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
    ``` 
1. устанавливаем параметры CORS в файле settings.py:
   
   Добавляем в список INSTALLED_APPS 'corsheaders'
   ```
    INSTALLED_APPS = [
        'corsheaders', # для настройки CORS запросов
    ]
   ```

   Добавляем в список MIDDLEWARE 'corsheaders.middleware.CorsMiddleware'
   ```
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware', # для настройки CORS запросов
    ]
   ```

   Создаем переменную CORS_ALLOW_ALL_ORIGINS
   ```
   CORS_ALLOW_ALL_ORIGINS = True # Разрешен доступ всем подключениям
   ```
1. создаем модели таблиц в нашем приложении, файл models.py
   - подготавливаем таблицы в джанго для миграции (**python manage.py makemigrations**)
   - запускаем миграцию таблиц (**python manage.py migrate**), при этом в директории migrations будет добавлен файл 0001_initial.py

2. если необходимо заполнить таблицу пользователей данными, тогда ввести команду **python manage.py loaddata users.json**
3. добавили urls для login и определили в views функцию отвечающую за это 