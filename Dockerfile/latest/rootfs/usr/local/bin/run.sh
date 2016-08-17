#!/bin/sh
addgroup -g ${GID} rufy && adduser -h /var/www/RuFy -s /bin/sh -D -G rufy -u ${UID} rufy

if [ $WEBROOT != "/" ]; then
    sed -i 's|<webroot>|'${WEBROOT}\/'|g' /etc/nginx/nginx.conf
    sed -i 's|<webroot2>|'${WEBROOT}'|g' /etc/nginx/nginx.conf
    sed -i -e '\#URI# s#/rufy#'${WEBROOT}'#' /var/www/RuFy/RuFy/settings.py
    sed -i -e '\#URI# s#rufy/#'${WEBROOT:1}'/#' /var/www/RuFy/RuFy/urls.py
else
    sed -i 's|<webroot>|/|g' /etc/nginx/nginx.conf
    sed -i 's|<webroot2>|/|g' /etc/nginx/nginx.conf
    sed -i -e '\#URI# s#/rufy##' /var/www/RuFy/RuFy/settings.py
    sed -i -e '\#URI# s#rufy/##' /var/www/RuFy/RuFy/urls.py
fi

if [ ! -f "/var/www/RuFy/db/db.sqlite3" ];then
    mv -v /var/www/RuFy/config/db-init.sqlite3 /var/www/RuFy/db/db.sqlite3
fi

mkdir -p /var/www/RuFy/log

/var/www/RuFy/venv/bin/python /var/www/RuFy/manage.py collectstatic_js_reverse
/var/www/RuFy/venv/bin/python /var/www/RuFy/manage.py makemigrations
/var/www/RuFy/venv/bin/python /var/www/RuFy/manage.py migrate

chown -R rufy:rufy /var/www/RuFy /watch /tmp

chmod +x /var/www/RuFy/gunicorn_start
sh /var/www/RuFy/gunicorn_start &

supervisord -c /usr/local/etc/supervisord.conf
