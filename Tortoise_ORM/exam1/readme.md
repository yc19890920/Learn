
## CREATE DATABASE tortoise DEFAULT CHARACTER SET utf8mb4;


数据迁移：
$ sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.8.0/dbmate-linux-amd64
$ sudo chmod +x /usr/local/bin/dbmate

/home/python/.pyenv/versions/fastapi/bin/python main.py 

/home/python/.pyenv/versions/fastapi/bin/python manage.py makemigrations --name tournament
/home/python/.pyenv/versions/fastapi/bin/python manage.py makemigrations --name name_max_length_64

/home/python/.pyenv/versions/fastapi/bin/python manage.py migrate

```
https://aur.archlinux.org/packages/schemalex-bin/
$ wget https://github.com/schemalex/schemalex/releases/download/v0.0.9/schemalex_linux_amd64.tar.gz
$ tar -ztvf schemalex_linux_amd64.tar.gz
$ tar -zxvf schemalex_linux_amd64.tar.gz
# cp schemalex_linux_amd64/schemalex /usr/local/bin/schemalex
$ sudo chmod +x /usr/local/bin/schemalex

https://github.com/amacneil/dbmate/releases
$ wget /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.8.0/dbmate-linux-amd64
# cp dbmate-linux-amd64 /usr/local/bin/dbmate && chmod +x /usr/local/bin/dbmate && rm -rf dbmate-linux-amd64
```



