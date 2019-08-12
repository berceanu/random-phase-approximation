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
$ conda install gunicorn
```

```console
$ cd ~/Development/random-phase-approximation/signac/projects/rpa/src
$ gunicorn --bind 0.0.0.0:5000 wsgi:dashboard
```

```
# /etc/systemd/system/rpa.service
[Unit]
Description=Gunicorn instance to serve random-phase-approximation/rpa
After=network.target

[Service]
User=berceanu
Group=www-data
WorkingDirectory=/home/berceanu/Development/random-phase-approximation/signac/projects/rpa/src
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

Adapted from [this guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04).

See also [how to configure `Nginx`](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)(and links therein).
