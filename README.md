Дипломная работа для fullstack-разработчика - облачное хранилище
===

## Backend

*Ссылка на git-hub репозиторий (backend):* https://github.com/darknessdizi/diploma_cloud_store_backend.git

## Fronted

Чтобы просмотреть работу клиентской части перейдите по ссылке ниже.

*Ссылка на страницу (fronted):* https://darknessdizi.github.io/diploma_cloud_store/

*Ссылка на git-hub репозиторий (fronted):* https://github.com/darknessdizi/diploma_cloud_store.git

## Инструкция по развертыванию проекта на сервере Linux Ubuntu

1. Для подключения к серверу через терминал необходимо сгенерировать ключ SSH. Для генерации ключа SSH в вашем терминале (в командной строке) введите команду:
```bash
ssh-keygen
```
- *Пример:*

   ![Генерация ключа](/pic/ssh.png)
- Если ключ создается впервые, то появятся запросы на ввод дополнительной информации (можно пропустить нажав enter).
Если ключ уже имеется, появится запрос на его перезапись. Введите y или n.
- Если ключ уже имеется, ввод команды `ssh-keygen` можно пропустить.


2. Для получения ключа SSH в терминале введите команду:
```bash
cat ~/.ssh/id_rsa.pub
```
- *Пример:*

   ![Получение ключа](/pic/ssh-key.png)
- После ввода команды `cat ~/.ssh/id_rsa.pub` в терминале отобразится ранее сгенерированный ключ SSH (пункт 2 на рисунке).
- Данный ключ необходимо скопировать и добавить в соответствующее поле при создании сервера.

3. Создайте сервер с операционной системой Ubuntu на выбранной Вами платформе и задайте ему скопируемый SSH ключ.
- *Например платформа reg.ru:*

   ![Добавление ключа серверу](/pic/server-ssh-key.png)

4. Войдите через консоль на Ваш сервер введя команду:
```bash
ssh root@0.0.0.0
```
- Где root это Ваш логин, который был Вам присвоен при создании сервера. 
- 0.0.0.0 это IP адрес Вашего сервера (пункт 1 на рисунке).

Логин, пароль для подключения и IP адрес будут направлены на Вашу электронную почту после создания сервера на платформе. При подключении консоль запросит у Вас пароль, который прислали Вам вместе с логином.
- *Пример подключения:*

  ![Подключение к серверу](/pic/connection2.png)

При первом подключении необходимо указать yes или no, на вопрос доверяете ли Вы данному хосту, к которому подключаетесь (пункт 2 на рисунке).

- *Пример:*

  ![Подключение к серверу](/pic/connection.png)

5. Создайте нового пользователя на сервере, для этого в консоли введите команду:
```bash
adduser user_name
```
Вместо user_name вводим имя нового пользователя (пункт 1 на рисунке). Прописываем ему пароль и общую информацию (пункт 2 на рисунке)
- *Пример:*

  ![Создание пользователя](/pic/superuser.png)

*Примечание: удалить пользователя можно командой `sudo deluser user_name`*

6. Наделите нового пользователя правами `superuser`, введите команду:
```bash
usermod user_name -aG sudo
```
7. Переключитесь на вновь созданного пользователя, введите команду:
```bash
sudo -i -u user_name
```
- *Пример:*

  ![Смена пользователя](/pic/replacement.png)
После ввода команды на смену пользователя (пункт 1 на рисунке) в строке ввода команд сменится имя пользователя (пункт 2 на рисунке).

8. Перед установкой основных пакетов на сервер обновите список репозиториев, введите команду:
```bash
sudo apt update -y
```
- При вводе команды запросит пароль пользователя которым Вы зашли.
- *Пример:*

  ![Обновление пакетов](/pic/update.png)

9. При необходимости можно обновить список пакетов, введите команду (можно пропустить, занимает много времени):
```bash
sudo apt upgrade -y
```

10.  Устанавливаем следующие пакеты на сервер, введите команду:
```bash
sudo apt-get install python3 python3-venv python3-pip postgresql nginx
```
- При вводе команды потребуется ввести пароль пользователя и дать согласие на установку.

11.  Проверить работоспособность и правильную установку postgresql и nginx, введите команду:
```bash
sudo systemctl status postgresql nginx
```
- *Пример:*

  ![Проверка установки](/pic/postgresql.png)
Оба пакета должны иметь статус `active`. Значит установка прошла без сбоев и пакеты работоспособны. Если пакет не имеет статус `active` необходимо выполнить команду для запуска процесса вручную:
```bash
sudo systemctl start postgresql
```

12. Создаем базу данных на сервере, для этого выполнить следующие действия:
      1. Перейти на системного пользователя postgres командой:
      ```bash
      sudo su postgres
      ```
      - *Пример:*

      ![Пользователя postgres](/pic/go-postgres.png)

      2.  Под пользователем postgres зайти в панель psql, ввести команду:
      ```bash
      psql
      ```
      - *Пример:*

      ![Панель psql](/pic/psql.png)

      3.  Задать пароль пользователю postgres:
      ```bash
      ALTER USER postgres WITH PASSWORD '12345678';
      ```
      - *Пример:*

      ![Пароль пользователю postgres](/pic/password.png)

      4.  Создать базу данных:
      ```bash
      CREATE DATABASE cloud_db;
      ```
      - *Пример:*

      ![Создать базу данных](/pic/create-db.png)

      5.  Выйти из панели psql, ввести команду:
      ```bash
      \q
      ```
      - *Пример:*

      ![Выход](/pic/exit-q.png)

      6.  Выйти из пользователя postgres командой:
      ```bash
      exit
      ```
      - *Пример:*

      ![Выход](/pic/exit-postgres.png)

13. Скопируйте репозиторий с проектом для сервера:
```bash
git clone https://github.com/darknessdizi/diploma_cloud_store_backend.git backend
```
- *Пример:*

![Копирование репозитория](/pic/clone.png)

После копирования проекта с помощью `git clone` (пункт 1 на рисунке) на сервере появится папка `backend` с проектом (пункт 2 на рисунке). Список папок можно получить командой `ls`, `ls -A` или `ls --all`

14. Перейти в появившуюся папку `backend`:
```bash
cd backend/
```

15.  Запустите виртуальное окружение для python:
```bash
python3 -m venv venv
```

16. Активируйте виртуальное окружение python:
```bash
source venv/bin/activate
```
- *Пример:*

![Виртуальное окружение](/pic/activate.png)

17. Установите зависимости проекта из файла requirements.txt:
```bash
pip install -r requirements.txt
```
- *Пример:*

![PIP](/pic/pip.png)

18. Сделайте миграции для базы данных:
```bash
python manage.py migrate
```
- *Пример:*

![migrate](/pic/migrate.png)

19.  Добавьте первого пользователя в базу данных (он же будет администратором) из файла users.json:
```bash
python manage.py loaddata users.json
```
- *Пример:*

![loaddata](/pic/load.png)

20. Настройте gunicorn. Выполните следующие действия:
    1. Создайте файл `gunicorn.service`, введите команду:
    ```bash
    sudo nano /etc/systemd/system/gunicorn.service
    ```
    - *Пример:*

    ![Nano](/pic/nano.png)
    - Данная команда создаст файл `gunicorn.service`.
    - Откроет содержимое файла в редакторе `nano` (На начальном этапе файл будет пустым).

    2.  Впишите следующий код и замените dima на имя вашего пользователя в системе:
    ```bash
    [Unit]
    Description=gunicorn
    After=network.target

    [Service]
    User=dima
    Group=www-data
    WorkingDirectory=/home/dima/backend
    ExecStart=/home/dima/backend/venv/bin/gunicorn --access-logfile -\
        --workers=3 \
        --bind unix:/home/dima/backend/project_cloud_storage/project.sock project_cloud_storage.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ``` 
    Нажмите `CTRL + S` для сохранения изменений и `CTRL + X` для выхода из редактора.
    - *Пример:*

    ![gunicorn настройки](/pic/nano-full.png)

    3.  Запустите gunicorn введя команду:
    ```bash
    sudo systemctl start gunicorn
    ```
    - *Пример:*

    ![Запуск gunicorn](/pic/reload.png)
    При вводе данной команды (пункт 1 на рисунке) выйдет предупреждение о необходимости перезапустить сервис (пункт 2 на рисунке). Выполните перезапуск командой:
    ```bash
    systemctl daemon-reload
    ```
    Появится запрос кем пройти аунтификацию. Выбирите из списка желаемый вариант и введите соответствующий пароль (пункт 4 на рисунке).


    4.  Добавьте gunicorn в автозагрузку командой:
    ```bash
    sudo systemctl enable gunicorn
    ``` 

    5.  Проверьте работу gunicorn:
    ```bash
    sudo systemctl status gunicorn
    ```
    - *Пример:*

    ![Статус gunicorn](/pic/status-gunicorn.png)
    Настройка gunicorn на этом завершена.

21. Запустите сервер, введите команду:
```bash
python manage.py runserver 0.0.0.0:8000
```
- *Пример:*

![Запуск сервера](/pic/run-server.png)

22. Выйти из папки backend, введите команду:
```bash
cd ..
```
- *Пример:*

![Выход из папки](/pic/exit-backend.png)

23. Скопируйте репозиторий для клиентской части в корень вашего сервера:
```bash
git clone https://github.com/darknessdizi/diploma_cloud_store.git frontend
```
- *Пример:*

![Копирование fronted](/pic/clone-fronted.png)

24. Настройте nginx. Выполните следующие действия:  
    1. Создать новый файл конфигурации:
    ```bash
    sudo nano /etc/nginx/sites-available/cloud-storage
    ```
    - Данная команда создаст файл `cloud-storage` и откроет его в редакторе nano (На начальном этапе файл будет пустым).

    2. Впишите следующий код, замените имя пользователя системы и ip сервера:
    ```bash
    server {
        listen 80;
        server_name 91.197.96.56;
        root /home/dima/fronted/dist;

        location /media/ {
            alias /home/dima/backend/project_cloud_storage/media/;
            default_type "image/jpg";
        }
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/dima/backend/project_cloud_storage/project.sock;
        }
    }
    ```

    3. Создайте символическую ссылку на конфиг
    ```bash
    sudo ln -s /etc/nginx/sites-available/cloud-storage /etc/nginx/sites-enabled
    ```

    4. Переопределите конфиг сервера nginx и проверьте его работоспособность:
    ```bash
    sudo systemctl reload nginx
    sudo systemctl status nginx
    ```
    5. Логи nginx:
    ```bash
    sudo nano /var/log/nginx/access.log
    sudo nano /var/log/nginx/error.log
    ```
### Настройка проекта завершена.
