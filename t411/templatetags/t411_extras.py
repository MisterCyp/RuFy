#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
import unicodedata

register = template.Library()

def stripaccents(value, arg=""):
    return ''.join((c for c in unicodedata.normalize('NFD', value) if unicodedata.category(c) != 'Mn'))

register.filter("stripaccents", stripaccents)

def stripspace(value, arg=""):
    return ''.join(value.split(" "))

register.filter("stripspace", stripspace)

def majFirst(value,arg=""):
    first = value[0].upper()
    return first+value[1:]
    
register.filter("majFirst", majFirst)

def taille(octet):
    if octet == "" or octet ==0 or octet == None: return "##"
    
    unit = ["o","Ko","Mo","Go","To"]
    octet = float(octet)
    for i in reversed(range(len(unit))):
        taille = int(octet/(1024**i))
        if taille :
            taille = octet/(1024**i)
            taille = "%.2f" %taille + " " + unit[i]
            break
    
    return taille
    
register.filter("taille", taille)

def div(nb1,nb2):
    nb1,nb2 = float(nb1), float(nb2) 
    if nb2 == 0:
        return "Inf"
    return "%.2f" %(nb1/nb2)
    
register.filter("div", div)

def sub(nb1,nb2):
    nb1,nb2 = float(nb1), float(nb2) 
    return "%.f" %(nb1-nb2)
    
register.filter("sub", sub)

def mult(nb1,nb2):
    nb1,nb2 = float(nb1), float(nb2) 
    return "%.f" %(nb1*nb2)
    
register.filter("mult", mult)