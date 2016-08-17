## mistercyp/rufy


#### Volumes
- **/watch** : Dossier watch de RuTorrent
- **/var/www/RuFy/log** : log des accès 
- **/var/www/RuFy/db** : base de données
- 
####Port
port utilisé dans le conteneur : 80 

#### Variables d'environnement
- WEBROOT : URI d'accès à RuFy (par défaut : /rufy)
- UID : uid de l'utilisateur qui lance RuFy (par défaut 1000)
- GID : groupe de l'utilisateur qui lance RuFy (par défaut 1000)

#### Comment l'utiliser ?
#####Docker Run:
```
docker run -d -p 1234:80 -e WEBROOT=/rufy -e UID=1000 -e GID=1000 -v /home/cyprien/seedbox/.watch:/watch --name rufy mistercyp/rufy
```
Accès :  http://votreIPouNDD.tld:1234/rufy

#####Docker-compose.yml :
```
nginx:
    container_name: nginx
    image: wonderfall/reverse
    ports:
      - "80:8000"
      - "443:4430"
    links:
      - rutorrent:rutorrent
      - rufy:rufy
    volumes:
     - /home/cyprien/docker/containers/nginx/sites:/sites-enabled
     - /home/cyprien/docker/containers/nginx/conf:/conf.d
     - /etc/letsencrypt:/certs
     - /home/cyprien/docker/containers/nginx/log:/var/log/nginx
     - /home/cyprien/docker/containers/nginx/www:/var/www/
     - /home/cyprien/docker/containers/nginx/passwds:/passwds

rutorrent:
    image: mistercyp/rutorrent
    container_name: rutorrent
    environment:
      - WEBROOT=/rutorrent
      - UID=1000
      - GID=1000
    ports:
      - "49184:49184"
      - "49184:49184/udp"
    volumes:
      - /home/cyprien/seedbox:/data
      - /home/cyprien/seedbox/rutorrent/rc:/home/torrent 
      - /home/cyprien/seedbox/rutorrent/log:/var/log/nginx 
rufy:
    container_name: rufy
    image: mistercyp/rufy
    environment:
      - UID=1000
      - GID=1000
      - WEBROOT=/rufy
    volumes:
      - /home/cyprien/docker/containers/nginx/log:/var/www/RuFy/log
      - /home/cyprien/seedbox/.watch:/watch
```
Nginx cong :
```
server {
  listen 8000;
  server_name ndd.tld;
  
  location /RPC{
         proxy_pass http://rutorrent:80;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Remote-Port $remote_port;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_redirect off;
        }
  location /rutorrent{
         proxy_pass http://rutorrent:80;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Remote-Port $remote_port;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_redirect off;
        }
        
     location /rufy{
         proxy_pass http://rufy:80;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Remote-Port $remote_port;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_redirect off;
        }          
}
```
