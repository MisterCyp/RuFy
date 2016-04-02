#!/usr/bin/bash

INSTALLDIR=$(readlink -f $(dirname $0))
USER=rufy
GROUP=web
VIRTUALDIR="venv"

mkdir -p ${INSTALLDIR}/log/

exec 2>${INSTALLDIR}/log/install.log

echo "
#########################################
##### Installation des dépendances : ####
#########################################
"

echo "
####################################
#####     python 2.7            ####
####################################
"
aptitude install -y python2.7

echo "
####################################
#####     python-virtualenv     ####
####################################
"
aptitude install -y python-virtualenv

echo "
####################################
#####     python-dev            ####
####################################
"
aptitude install -y python-dev

echo "
####################################
#####     supervisor            ####
####################################
"
aptitude install -y supervisor

echo "
###########################################################################
#####     Création de l'utilisateur $USER associé au groupe $GROUP     ####
###########################################################################
"

groupadd $GROUP
useradd --system --gid $GROUP --shell /bin/bash --home $INSTALLDIR $USER


echo "
###########################################################################
#####     Configuration de supervisor pour lancer automatique RuFy     ####
###########################################################################
"
cd $INSTALLDIR
touch config/${USER}_SUPERVISOR.conf

echo "[program:rufy]
command = ${INSTALLDIR}/gunicorn_start                    ; Command to start app
user = ${USER}                                                          ; User to run as
stdout_logfile = ${INSTALLDIR}/log/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
environment=LANG=fr_FR.UTF-8,LC_ALL=fr_FR.UTF-8                       ; Set UTF-8 as default encoding" >> config/${USER}_SUPERVISOR.conf

cp config/${USER}_SUPERVISOR.conf /etc/supervisor/conf.d/${USER}_SUPERVISOR.conf
touch log/gunicorn_supervisor.log 

supervisorctl reread
supervisorctl update

echo "
###########################################################################
#####           Copie de la base de donnée initiale                    ####
###########################################################################
"

cp ${INSTALLDIR}/config/db-init.sqlite3 ${INSTALLDIR}/db.sqlite3

echo "
###########################################################################
#####     Configuration de Python pour RuFy avec virtualenv            ####
###########################################################################
"
mkdir -p $VIRTUALDIR

echo "
####################################################
$USER devient propriétaire du dossier $INSTALLDIR :
####################################################
"

chown -R ${USER}:users $INSTALLDIR
chmod -R g+w $INSTALLDIR
chmod +x ${INSTALLDIR}/gunicorn_start

echo "
####################################################
Creation du dossier virtualvenv dans $VIRTUALDIR 
####################################################
"
sudo su $USER -c "virtualenv -p /usr/bin/python2.7 $VIRTUALDIR"


echo "
#######################################
Activation du dossier virtualvenv 
#######################################
"
source ${VIRTUALDIR}/bin/activate

echo "
#####################################
Installation des requirements 
#####################################
"
pip install -r requirements.txt
pip install setproctitle

echo "
#####################################
Migrations Django
#####################################
"

python manage.py makemigrations
python manage.py migrate

echo "
################################################################################################################
Installation réussi : Il reste la configuration de Nginx pour rediriger les requetes vers 127.0.0.1:8000
################################################################################################################
"