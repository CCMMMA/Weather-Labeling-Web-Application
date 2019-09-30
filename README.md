# Weather Labelling Web Application

This software allows to identify different sensitive weather event in the Mediterranean Sea; in fact you will be able to locate a storm with a specific polygon. This polygon will have its own pop-up where insert a specific weather label on leaflet map. 
The user can watch different parameters :
A) cloud,
B) temperature at 2m,
C) rain,
D) snow,
e) wind.

These data are provided thanks to ajax calls in the meteo-uniparthenope library: this library belogs to "Università degli studi di Napoli Parthenope".

1 - Configuration:

- It is necessary to install mongodb and create a collection for users with unique username:
you type this command "db.UserCollection.createIndex( { "username": 1 }, { unique: true } )"

- It's necessary to insert the first admin by mongo's shell:
for example you could type this command --> db.UserCollection.insert({"name":"YOUR_NAME","surname":"YOUR_SURNAME","username":"YOUR_USERNAME","password":"YOUR_PASSWORD","role":"ADMIN"})

- If you wanted to remove "Uniparthenope" logo you would set flag = false in view.py in function index
