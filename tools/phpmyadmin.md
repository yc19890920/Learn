
- [Ubuntu16.04 安裝 Apache+PHP 7.1+MySQL+phpMyAdmin](https://bleuren.me/252/ubuntu-php-7-1/)
- [Ubuntu 16.04 (LTS) LAMP server tutorial with Apache, PHP 7, and MySQ](https://www.howtoforge.com/tutorial/install-apache-with-php-and-mysql-on-ubuntu-16-04-lamp/)
- [ubuntu 16.04 安装PhpMyAdmin](http://blog.csdn.net/l6807718/article/details/51374915)

systemctl restart apache2.service

/etc/apache2/conf-enabled/phpmyadmin.conf

```
Alias /phpmyadmin /usr/share/phpmyadmin

<Directory /usr/share/phpmyadmin>
 Options FollowSymLinks

DirectoryIndex index.php
AllowOverride None
Order allow,deny
Allow from all
Require all granted


# Only allow connections from localhost:
Require local

<IfModule mod_php5.c>
  php_flag magic_quotes_gpc Off
  php_flag track_vars On
  #php_value include_path .
</IfModule>
<IfModule !mod_php5.c>
  <IfModule mod_actions.c>
    <IfModule mod_cgi.c>
      AddType application/x-httpd-php .php
      Action application/x-httpd-php /cgi-bin/php
    </IfModule>
    <IfModule mod_cgid.c>
      AddType application/x-httpd-php .php
      Action application/x-httpd-php /cgi-bin/php
    </IfModule>
  </IfModule>
</IfModule>

</Directory>
```