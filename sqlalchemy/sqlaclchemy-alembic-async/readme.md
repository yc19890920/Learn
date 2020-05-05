##  创建数据库
CREATE DATABASE sql_alembic_aio DEFAULT CHARACTER SET UTF8;

## 生成迁移目录
alembic init YOUR_ALEMBIC_DIR
alembic init migrations

## 生成迁移文件
### 其中 "First create user add role table" 是这次迁移脚本的备注，类似git commit的message
alembic revision --autogenerate -m "First create user add role table"

## 升级 数据库为最新版本
alembic upgrade head
