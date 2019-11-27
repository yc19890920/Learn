#!/usr/bin/env bash
# 检测mysql是否启动

set -o errexit
set -o pipefail

echo $MYSQL_PASSWORD
echo $MYSQL_DATABASE
echo $MYSQL_HOST
echo $MYSQL_USER
echo $MYSQL_PORT

function mysql_ready(){
python << END
import sys
import pymysql
try:
    conn = pymysql.connect(host="$MYSQL_HOST", port=3306, user="root", passwd="$MYSQL_ROOT_PASSWORD", db='$MYSQL_DATABASE', charset='utf8')
except pymysql.err.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until mysql_ready; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - continuing..."