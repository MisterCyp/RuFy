#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

app_name = 't411'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
    url(r'^config/t411$', views.configT411, name='configT411'),
    url(r'^config/rutorrent$', views.configRut, name='configRut'),
    url(r'^config/menu$', views.configMenu, name='configMenu'),
    url(r'^top/$', views.top_torrents, name='top_torrents'),
    url(r'^top/(?P<type_top>\w+)$', views.top_torrents, name='top_torrents'),
    url(r'^torrent/(?P<id_torrent>\d+)$', views.detail_torrent, name='detail_torrent'),
    url(r'^search$', views.search, name='search'),
    url(r'^search/(?P<search>[\w\ ]+)/$', views.search, name='search'),
    url(r'^search/(?P<search>[\w\ ]+)/(?P<cid>\d+)$', views.search, name='search'),
    url(r'^search/(?P<search>[\w\ ]+)/(?P<cid>\d+)/(?P<page>\d+)$', views.search, name='search'),
    url(r'^download/(?P<id_torrent>\d+)-(?P<cid>\d+)$', views.download, name='download'),
]