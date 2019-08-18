# Initial setup for `Nginx` + `Gunicorn` + `signac-dashboard`

## Install dependencies

This guide assumes a working Ubuntu 18.04 installation.

```console
$ sudo apt update
$ sudo apt install nginx
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
$ sudo apt install python3-venv
```

## Configure `Gunicorn`

```console
$ conda activate random-phase-approximation
```

First, test `gunicorn` via

```console
$ cd ~/Development/random-phase-approximation/signac/projects/rpa/src
$ gunicorn --bind 0.0.0.0:5000 wsgi:dashboard
```

```
# /etc/systemd/system/rpa.service
[Unit]
Description=Gunicorn instance to serve computed dipole strengths
After=network.target

[Service]
User=berceanu
Group=www-data
WorkingDirectory=/home/berceanu/Development/rpa/projects/rpa/src
Environment="PATH=/home/berceanu/miniconda3/envs/random-phase-approximation/bin"
ExecStart=/home/berceanu/miniconda3/envs/random-phase-approximation/bin/gunicorn --workers 3 --bind unix:rpa.sock -m 007 wsgi:dashboard

[Install]
WantedBy=multi-user.target
```

```console
$ sudo systemctl start rpa
$ sudo systemctl enable rpa
$ sudo systemctl status rpa
```

**Notes**: 

1) Add multiple services by changing the respective paths above and follow the same steps to enable them.
1) Remember to run `sudo systemctl daemon-reload` after each repo update.

## Configure `Nginx`

```
# /etc/nginx/sites-available/rpa
server {
    listen 80;
    listen [::]:80;

    server_name rpa.ra5.ro www.rpa.ra5.ro;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/berceanu/Development/random-phase-approximation/signac/projects/rpa/src/rpa.sock;
    }
}
```

```console
$ sudo ln -s /etc/nginx/sites-available/rpa /etc/nginx/sites-enabled
$ sudo nginx -t
$ sudo systemctl restart nginx
```

**Notes**

1) Add more subdomains by changing the sock path above and making the respective symlinks.
1) The subdomains need to have correct DNS A-record entries.
1) The max socks path length is 107 chars.

### Add page to root domain with links to subdomains

```console
$ sudo mkdir -p /var/www/ra5.ro/html
$ sudo chown -R $USER:$USER /var/www/ra5.ro/html
$ sudo chmod -R 755 /var/www/ra5.ro
$ vi /var/www/ra5.ro/html/index.html
```

```html
<html>
    <head>
        <title>ra5.ro</title>
    </head>
    <body>
        <h1><a href="http://rpa.ra5.ro">rpa</a></h1>
        <h1><a href="http://rpa.agg.ra5.ro">rpa-aggregation</a></h1>
        <h1><a href="http://rpa.agg.anim.ra5.ro">rpa-animation</a></h1>
    </body>
</html>
```

```console
$ sudo vi /etc/nginx/sites-available/ra5.ro
```

```
# /etc/nginx/sites-available/ra5.ro
server {
        listen 80;
        listen [::]:80;

        root /var/www/ra5.ro/html;
        index index.html index.htm index.nginx-debian.html;

        server_name ra5.ro www.ra5.ro;

        location / {
                try_files $uri $uri/ =404;
        }
}
```

```console
$ sudo ln -s /etc/nginx/sites-available/ra5.ro /etc/nginx/sites-enabled/
$ sudo vi /etc/nginx/nginx.conf
```

```
# /etc/nginx/nginx.conf
...
http {
    ...
    server_names_hash_bucket_size 64;
    ...
}
...
```

```console
$ sudo nginx -t
$ sudo systemctl restart nginx
```

Adapted from [this guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04).

See also [how to configure `Nginx`](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)(and links therein).
