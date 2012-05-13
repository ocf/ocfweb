#!/bin/sh

python setup.py install --home=/usr/local/www/django_projects

cp -f public_html/account_tools/{.htaccess,account_tools.fcgi} /mnt/http/localhost

cd /usr/local/www/django_projects/lib/python
cp /root/account_tools_settings.py.secret account_tools/settings.py
chown -R www:www account_tools
chmod -R o-rwx account_tools

