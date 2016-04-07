#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from t411.models import Profil, Menu
from django.forms import ModelForm, TextInput


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    
class ConfigForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur T411")
    password = forms.CharField(label="Mot de passe (non stocké)", widget=forms.PasswordInput)
    dossier  = forms.CharField(label="Dossier blackhole Rutorrent")
    
class T411Form(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ('pseudoT411',)
    
    password = forms.CharField(label="Mot de passe (non stocké)", widget=forms.PasswordInput)

class DossierForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ('dossier',)
        widgets = {
            'dossier': TextInput(attrs={'size': 80}),
        }
        
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('nom','lien')
        widgets = {
            'nom': TextInput(attrs={'size': 15}),
            'lien': TextInput(attrs={'size': 25})
        }