#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

import getpass
import json
import requests
from requests.auth import HTTPDigestAuth

        
class Profil(models.Model):
    user = models.OneToOneField(User)  # La liaison OneToOne vers le modèle User
    dossier = models.CharField(max_length=200,null=True, blank = True)
    
    pseudoT411 = models.CharField(max_length=42,null=True)
    uid = models.IntegerField(null=True)
    token = models.CharField(max_length=50,null=True)
    downloaded = models.IntegerField(null=True, default=0)
    uploaded = models.IntegerField(null=True, default=0)
    
    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Menu(models.Model):
    nom = models.CharField(max_length=15)
    lien = models.CharField(max_length=500)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, default=0)
    
    def __str__(self):
        return "Menu de {0}. Nom : {1}".format(self.profil,self.nom)
  
class Categorie(models.Model):
    pid = models.IntegerField()
    nom = models.CharField(max_length=40,null=True)
    
    def __str__(self):
        return "{0}".format(self.nom.encode('utf-8'))
        
class SousCategorie(models.Model):
    pid = models.ForeignKey(Categorie, on_delete=models.CASCADE,null=True)
    cid = models.IntegerField()
    nom = models.CharField(max_length=40, null=True)
    
    def __str__(self):
        return "{0}".format(self.nom.encode('utf-8'))

class Folder(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, default=0)
    dossier = models.CharField(max_length=40,null=True)
    cid = models.IntegerField()

    def __str__(self):
        return "{0} : Dossier pour la categorie {1}".format(self.profil, str(self.cid))
        
HTTP_OK = 200
API_URL = 'http://api.t411.li/%s'

class T411(Profil):
    """ Base class for t411 interface """
    
    def __init__(self, profil) :
        """ Get user credentials and authentificate it, if any credentials
        defined use token stored in user file
        """ 
        self.profil = profil

    def get_token(self, username, password) :
        """ Authentificate user and store token """
        self.user_credentials = self.call('auth', {'username': username, 'password': password})

        return self.user_credentials

    def call(self, method = '', params = None) :
        """ Call T411 API """
        call_params = {'url': API_URL % method, 'params': params}
        if method != 'auth' :
            req = requests.get(call_params['url'],headers={'Authorization': self.profil.token})
        else: req = requests.post(call_params['url'],data = call_params['params'])
        
        if req.status_code == requests.codes.OK:
            if method.startswith('torrents/download/') :
                return req
            else: return req.json()
        else :
            print ('Error while sending %s request: HTTP %s' % \
                    (method, req.status_code))

    def me(self) :
        """ Get personal informations """
        return self.call('users/profile/%s' % self.profil.uid)
    def get_info(self):
        info = self.me()
        if 'error' in info:
            return False 
        else :
            self.profil.downloaded = info['downloaded']
            self.profil.uploaded = info['uploaded']
            self.profil.save()
            return True

    def user(self, user_id) :
        """ Get user informations """
        return self.call('users/profile/%s' % user_id)

    def categories(self) :
        """ Get categories """
        return self.call('categories/tree')

    def terms(self) :
        """ Get terms """
        return self.call('terms/tree')

    def details(self, torrent_id) :
        """ Get torrent details """
        return self.call('torrents/details/%s' % torrent_id)

    def download(self, torrent_id) :
        """ Download a torrent """
        return self.call('torrents/download/%s' % torrent_id)
        
    def top100(self):
        """ Get top 100 of torrents """
        return self.call('/torrents/top/100')

    def topToday(self):
        """ Get top 100 of torrents """
        return self.call('/torrents/top/today')
    
    def topWeek(self):
        """ Get top 100 of torrents """
        return self.call('/torrents/top/week')
    
    def topMonth(self):
        """ Get top 100 of torrents """
        return self.call('/torrents/top/month')
        
    def search(self,search ="avatar",options = {"offset":0,"limit":20}):
        
        criteres="?"
        for cle, valeur in options.items():
            criteres += cle+"="+str(valeur)+"&"
        criteres = criteres[:-1]
        requete = search + criteres
        
        return self.call('/torrents/search/%s' %requete)
    
    def extraire(self,fonction = "top100" ,category="Film",limit=10,seedersMin = 0):
        
        torrents = getattr(self, fonction)()
        result = []
        i = 1
        for torrent in torrents:
            if torrent['categoryname'] == category and int(torrent['seeders'])>=seedersMin:
                result.append(torrent)     
                i += 1
            if i>limit: break
        return result
