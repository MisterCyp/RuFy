# RuFy
Web-application to download T411 Tracker's torrents from your seedbox

## Installation

You have to be connected in Root :

```sh
$ cd /var/www/
$ git clone https://github.com/MisterCyp/RuFy.git
```

```sh
$ chmod +x RuFy/install.sh
$ ./RuFy/install.sh
```

### Nginx config :
```sh
upstream rufy_server {
  server unix:/var/www/RuFy/run/gunicorn.sock fail_timeout=0;
}

server {
    ## Your config ##
    ## .....       ##
    ## End of your config ##
    
    location ^~/rufy/static {
        satisfy any;
	    allow all;
        alias /var/www/RuFy/static/;
    }
    
    location ^~/rufy/media {
        satisfy any;
	    allow all;
        alias    /var/www/RuFy/media/;
    }

    location ^~/rufy {
        satisfy any;
	    allow all;
	    
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
        }
    }
}
```

```sh
$ supervisorctl start rufy
$ service nginx restart
```
Access to RuFy : yourdomain.tld/rufy

### Create User
You have to create a new user :
Connect to yourdomain.tld/rufy/admin 

User : admin
Password : motdepasse

Think to change the password of admin

![](http://img15.hostingpics.net/pics/944456confFury.png)

### Define T411 account

![](http://img15.hostingpics.net/pics/747357t411.png)

### Define Folder for RuTorrent

![](http://img15.hostingpics.net/pics/761158dossier.png)

Give the rights to web group to write in this folder :

```sh
$ chown user1:web /home/user1/watch
$ chmod g+w /home/user1/watch
```

### Commands
```sh
$ supervisorctl start rufy # To start rufy
$ supervisorctl stop rufy # To stop rufy
```

## Configs
Port by default : 8000






