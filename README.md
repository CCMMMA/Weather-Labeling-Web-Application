# Weather Labeling Web Application

This software allows to identify different sensitive weather event in the Mediterranean Sea; in fact you will be able to locate a storm with a specific polygon. This polygon will have its own pop-up where insert a specific weather label on leaflet map. 
The user can watch different parameters :
A) cloud,
B) temperature at 2m,
C) rain,
D) snow,
e) wind.

These data are provided thanks to ajax calls in the meteo-uniparthenope library: this library belogs to "Università degli studi di Napoli Parthenope".

Configuration:

1. git clone https://github.com/CCMMMA/Weather-Labeling-Web-Application
2. cd Weather-Labeling-Web-Application/
3. virtualenv venv
4. source venv/bin/activate
5. pip install --upgrade pip
6. pip install -r requirements.txt
7. export FLASK_APP=app.py
8. export FLASK_DEBUG=true
you must install mongo db and execute these commands in mongo shell:

- db.UserCollection.createIndex( { "username": 1 }, { unique: true } )
- db.LabelCollection.createIndex( { "labelId": 1 }, { unique: true } )
- db.LabelCollection.createIndex( { "labelName": 1 }, { unique: true } )
- db.PolygonCollection.createIndex({"geometry.coordinates":1,"properties.dateStr":1},{unique:true})

9. It's necessary to insert the first admin by mongo's shell:
for example you could type this command:

- db.UserCollection.insert({"name":"YOUR_NAME","surname":"YOUR_SURNAME","username":"YOUR_USERNAME","password":"YOUR_PASSWORD","role":"ADMIN"})

10. You must insert your secret key in views.py --> app.secret_key = 'Your_secret_string'; for example you could create your secret key using python:

- python
- import os
- os.urandom(24)
- quit()
- vi views.py

11. insert your path where there are netCDF file in myfunction.py --> localPath = "<insert your path where there are netCDF file>"
 
12. install server redis; for example for Ubuntu OS:

- sudo apt update
- sudo apt install redis-server

13. flask run --host 0.0.0.0  --port 5555
14. In another terminal in same path lauch this command: celery -A app.celery worker -l info
15. If you wanted to remove "Uniparthenope" logo you would set flag = false in view.py in function index
