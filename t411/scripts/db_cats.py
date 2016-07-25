python manage.py shell

from t411.models import *
import json
json_data=open('t411\scripts\categories.json')
data = json.load(json_data)

for key, value in data.items():
    if value.get('name'):
        cat = Categorie.objects.get_or_create(pid = key)[0]
        cat.nom = value.get('name').encode('utf-8')
        cat.save()
        
        for cid, dict in value.get('cats').items():
            scat = SousCategorie.objects.get_or_create(cid = cid)[0]
            scat.pid = cat
            scat.cid = cid
            scat.nom = dict.get('name').encode('utf-8')
            scat.save()