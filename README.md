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
- Пример:
![Генерация ключа](/pic/ssh.png)
- Если ключ создается впервые, то появятся запросы на ввод дополнительной информации (можно пропустить нажав enter).
Если ключ уже имеется, появится запрос на его перезапись. Введите y или n.
- Если ключ уже имеется, ввод команды `ssh-keygen` можно пропустить.


2. Для получения ключа SSH в терминале введите команду:
```bash
cat ~/.ssh/id_rsa.pub
```
- Пример:
![Получение ключа](/pic/ssh-key.png)
- После ввода команды `cat ~/.ssh/id_rsa.pub` в терминале отобразится ранее сгенерированный ключ SSH (пункт 2 на рисунке).
- Данный ключ необходимо скопировать и добавить в соответствующее поле при создании сервера.

3. Создайте сервер с операционной системой Ubuntu на выбранной Вами платформе и задайте ему скопируемый SSH ключ.
- Например платформа reg.ru:
![Добавление ключа серверу](/pic/server-ssh-key.png)

4. Войдите через консоль на Ваш сервер введя команду:
```bash
ssh root@0.0.0.0
```
- Где root это Ваш логин, который был Вам присвоен при создании сервера. 
- 0.0.0.0 это IP адрес Вашего сервера (пункт 1 на рисунке).

Логин, пароль для подключения и IP адрес будут направлены на Вашу электронную почту после создания сервера на платформе. При подключении консоль запросит у Вас пароль, который прислали Вам вместе с логином.
- Пример подключения:
![Подключение к серверу](/pic/connection2.png)

При первом подключении необходимо указать yes или no, на вопрос доверяете ли Вы данному хосту, к которому подключаетесь (пункт 2 на рисунке).

- Пример:
![Подключение к серверу](/pic/connection.png)

5. Создайте нового пользователя на сервере, для этого в консоли введите команду:
```bash
adduser user_name
```
Вместо user_name вводим имя нового пользователя (пункт 1 на рисунке). Прописываем ему пароль и общую информацию (пункт 2 на рисунке)
- Пример:
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
- Пример:
![Смена пользователя](/pic/replacement.png)
После ввода команды на смену пользователя (пункт 1 на рисунке) в строке ввода команд сменится имя пользователя (пункт 2 на рисунке).

8. Перед установкой основных пакетов на сервер обновите список репозиториев, введите команду:
```bash
sudo apt update -y
```
- При вводе команды запросит пароль пользователя которым Вы зашли.
- Пример:
![Обновление пакетов](/pic/update.png)

9. При необходимости можно обновить список пакетов, введите команду (можно пропустить, занимает много времени):
```bash
sudo apt upgrade -y
```

10. Устанавливаем следующие пакеты на сервер, введите команду:
```bash
sudo apt-get install python3 python3-venv python3-pip postgresql nginx
```
- При вводе команды потребуется ввести пароль пользователя и дать согласие на установку.

11. Проверить работоспособность и правильную установку postgresql и nginx, введите команду:
```bash
sudo systemctl status postgresql nginx
```
- Пример:
![Проверка установки](/pic/postgresql.png)
Оба пакета должны иметь статус `active`. Значит установка прошла без сбоев и пакеты работоспособны. Если пакет не имеет статус `active` необходимо выполнить команду:
```bash
sudo systemctl start postgresql
```
Для запуска процесса вручную.

12.  Создаем базу данных на сервере, для этого выполнить следующие действия:
     1. Перейти на системного пользователя postgres командой:
      ```bash
      sudo su postgres
      ```
      2. Под пользователем postgres зайти в панель psql, ввести команду:
      ```bash
      psql
      ```
      3. Задать пользователю postgres пароль:
      ```bash
      ALTER USER postgres WITH PASSWORD '112233';
      ```
      4. Создать базу данных:
      ```bash
      CREATE DATABASE cloudDB;
      ```
      5. Выйти из панели psql, ввести команду:
      ```bash
      \q
      ``` 
      6. Выйти из пользователя postgres, командой:
      ```bash
      exit
      ```