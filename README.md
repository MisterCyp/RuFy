# RuFy
Web-application to download T411 Tracker's torrents from your seedbox


## Particularité de la branche torrentStream
Cette branche est encore à l'étape de la preuve de concept. Elle permet de streamer directement dans le navigateur un torrent est de l'afficher dans un player. Pour ce faire un nouveau backend en nodejs a été implémenter utilisant la librairie webTorrent. 

### Procédure de fonctionnement
- Lancer apache ou nginx comme d'habitude. 
- installer les dependances du backend nodejs. pour ce faire, aller dans le dossier nodejs, et executer :
```sh
sudo npm install
```

- Lancer le backend nodejs. Si vous utiliser le module wsgi pour lancer rufy, il faut executer :
```sh
sudo -H -u www-data -c 'node /var/www/rufy/nodejs/index.js'
```
ou 
```sh
sudo -H -u rufy -c 'node /var/www/rufy/nodejs/index.js'
```
Si vous êtes sous nginx, ou si vous avez mis rufy derrière un reverse proxy. 

-Il faut ensuite, dans rufy, configurer le dossier de téléchargement temporaire. Cette config ce trouve sous le même menu que la configuration du dossier de téléchargement en blackhole de rutorrent (le nom du dossier doit finir par un '/'), conseillé (/var/www/rufy/nodejs/assets/)

-Il ne vous reste plus qu'a aller sur votre torrent, et de cliquer sur streaming.

### Limitation de la POC
- Pour le moment, le stream ne fonctionne que sur les fichier mp4. Donc bien choisir un torrent en mp4 (les mkv ne fonctionneront pas)
- Le backend est encore bugué de partout, donc s'assurer que la stdout de la console n'affiche pas d'erreur. Si vous rencontreze des erreurs dans le fonctionnement, merci d'ouvrir une issue la plus explicite possible afin que je puiise reproduire le bug, et fixée tout cela au fure et à mesure. 
- Le port utilisé par nodejs doit être ouvert (port 3000 par défaut) afin que le client puisse récuperer le fichier video en cours de stream).
- Il n'y a aucune loading screen pour le moment, donc la video peut mettre un certain temps à s'afficher (dépendant de votre connexion internet). Si elle met vraiment trop de temps, ouvrir le débuggueur de votre navigateur, est assurer vous qu'il n'y a pas d'erreur 500 ou 404 vers les requêtes sur le backend nodejs (les paths finissent pas /torrentstream, ça vous aidera à les voir). Si il y a bien une erreur, relancer le backend et actualisé la page
- N'a pas l'air de fonctionner sur un navigateur mobile pour le moment. Bug a corriger car il n'y a pas de raison à cela.

### TODO
- Corriger les nombreux bugs possible. 
- Ajouter la loading screen, ainsi qu'un peu plus de verbose sur les differentes erreurs possible directement dans la page web.
- Afficher le status du backend nodejs sur la page web, et pouvoir le relancer depuis la page web en cas de problème.
- Mettre en place du la conversion à la volée du flux video, dans le cas ou la video n'est pas compatible avec html5 (pour les mkv par exemple).
- Ajouter de l'info, via websocket, sur le nombre de peer connecté, la vitesse d'UP et de DOWN, etc... 

### Invitation
Je ne suis pas un expert du javascript, ni du nodejs. Si quelqu'un à envie de s'impliquer, n'hésitez pas à forker ce repo, et à proposer des améliorations. Elles sont bien evidemment les biencenues. 

## Installation
### Via Docker

See https://github.com/MisterCyp/dockerfiles/tree/master/rufy

### Directly
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






