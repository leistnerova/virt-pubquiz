* Installing
** Apache setting
<VirtualHost *:80>

    WSGIScriptAlias /virt-pubquiz /var/www/wsgi-scripts/virt-pubquiz/virt-pubquiz.wsgi

    <Directory /var/www/wsgi-scripts>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
    </Directory>
</VirtualHost>

** SeLinux
semanage fcontext -a -t httpd_sys_rw_content_t "/var/www/wsgi-scripts/virt-pubquiz/virt_pubquiz/files(/.*)?"
restorecon -v /var/www/wsgi-scripts/virt-pubquiz/virt_pubquiz/files
