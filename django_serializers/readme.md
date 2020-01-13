https://www.django-rest-framework.org/api-guide/relations/
https://www.django-rest-framework.org/api-guide/fields/
https://www.jianshu.com/p/82df4bc4ff27
https://blog.csdn.net/l_vip/article/details/79156113
https://blog.csdn.net/qq_34374753/article/details/84941953


/home/python/pyenv/versions/opene/bin/python
/home/python/pyenv/versions/opene/bin/pip

cd /home/python/git/django2
/home/python/pyenv/versions/opene/bin/django-admin.py startproject opene

mysql -uroot -p123456
CREATE DATABASE test DEFAULT CHARACTER SET UTF8;
create user 'test'@'%' identified by '123456';
GRANT ALL ON test.* TO 'test'@'%';
flush  privileges;

/home/python/pyenv/versions/opene/bin/python /home/python/Learn/django_serializers/opene/manage.py startapp test
/home/python/pyenv/versions/opene/bin/python /home/python/Learn/django_serializers/opene/manage.py makemigrations
/home/python/pyenv/versions/opene/bin/python /home/python/Learn/django_serializers/opene/manage.py migrate
/home/python/pyenv/versions/opene/bin/python /home/python/Learn/django_serializers/opene/manage.py createsuperuser
admin/1qaz@WSX

关闭防火墙： sudo ufw disable
/home/python/pyenv/versions/opene/bin/python /home/python/Learn/django_serializers/opene/manage.py runserver 0.0.0.0:8069

## 备份数据库
mysqldump -uroot -p123456 test > ~/Learn/django_serializers/opene/data.sql

## 数据还原
mysql -uroot -p123456 test < ~/Learn/django_serializers/opene/data.sql


验证错误返回格式

umail:
    serializers.ValidationError
    UniqueValidator
    UniqueTogetherValidator
    
    validate_name
    validate_email
    
    
## list:
{
    "status": 200,
    "msg": "OK",
    "data": {
        "count": 0,
        "next": null,
        "previous": null,
        "results": [ ]
    },
    "code": "0000"
}

{
    "status": 200,
    "msg": "OK",
    "data": {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
            {
                "id": 1,
                "name": "杨向晴",
                "name2": "",
                "email": "1248644045@qq.com",
                "order_no": "aa",
                "province": "aa",
                "amount": "1.00",
                "permmisson": 1,
                "disabled": 2,
                "created": "2019-12-14T04:33:34",
                "updated": "2019-12-14T04:33:34"
            }
        ]
    },
    "code": "0000"
}

## create 正确结果
{
    "status": 200,
    "msg": "success",
    "data": {
        "id": 1,
        "name": "杨向晴",
        "name2": "",
        "email": "1248644045@qq.com",
        "order_no": "aa",
        "province": "aa",
        "amount": "1.00",
        "permmisson": 1,
        "disabled": 2,
        "created": "2019-12-14T04:33:34",
        "updated": "2019-12-14T04:33:34"
    },
    "code": "0000"
}

错误提示：
{
    "status": 400,
    "msg": "名称已存在！",
    "data": {
        "name": [
            "名称已存在！"
        ]
    },
    "code": "unique"
}

{
    "status": 400,
    "msg": "邮箱和订单号唯一",
    "data": {
        "non_field_errors": [
            "邮箱和订单号唯一"
        ]
    },
    "code": "unique"
}

{
    "status": 400,
    "msg": "name2不能为空！",
    "data": {
        "name2": [
            "name2不能为空！"
        ]
    },
    "code": "invalid"
}


## /api/test/1/
{
    "status": 200,
    "msg": "OK",
    "data": {
        "id": 1,
        "name": "杨向晴",
        "name2": "",
        "email": "1248644045@qq.com",
        "order_no": "aa",
        "province": "aa",
        "amount": "1.00",
        "permmisson": 1,
        "disabled": 2,
        "created": "2019-12-14T04:33:34",
        "updated": "2019-12-14T04:33:34"
    },
    "code": "0000"
}

## /api/test/2/
{
    "status": 404,
    "msg": "Not Found",
    "data": {
        "detail": "Not found."
    },
    "code": "0004"
}

## postman
postman 指定 Content-Type： application/json, Accept： application/json
Body 指定 raw, 并且 JSON, 每个字段必须以双引号，不能为单引号。

{
	"email": "1248644045@qq.com",
	"name": "杨向晴",
	"name": "aa",
	"order_no": "aa",
	"province": "aa"
}   

postman 指定 Content-Type： multipart/form-data, Accept： application/json
Body 指定 form-data，维护数据键值对。


## http://192.168.181.135:8069/api/test/goods/
postman 指定 Content-Type： application/json, Accept： application/json
Body 指定 raw, 并且 JSON, 每个字段必须以双引号，不能为单引号。

{
    "goods": [
        {
            "name": "aa",
            "amount": 10.5
        },
        {
            "name": "bb",
            "amount": 0.5
        }
    ]
}


    

