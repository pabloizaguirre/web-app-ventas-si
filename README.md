# VideoClub

Vintage inspired videoclub web application that provides a movie selling service. Vintage, just as videoclubs. 

It uses the Flask framework for python and makes use of a postgreSQL
database. Will integrate a MongoDB noSQL database in the future. 

### Set up

```
virtualenv -p python3 si1pyenv
source si1pyenv/bin/activate
pip3 install Flask SQLAlchemy Flask-SQLAlchemy SQLAlchemy-Utils \ psycopg2 itsdangerous Flask-Session 
python3 -m app
```

### Web application demonstration

Home screen:

<img width="1392" alt="Captura de pantalla 2022-11-22 a las 0 40 09" src="https://user-images.githubusercontent.com/47717915/203179858-366498ef-5464-4f6b-88fb-61c5be9a265a.png">

Movie details: 

<img width="1392" alt="Captura de pantalla 2022-11-22 a las 0 49 27" src="https://user-images.githubusercontent.com/47717915/203180919-80e1d30c-33d3-4401-8f86-b0eb19edfe57.png">

Wishlist: 

<img width="1392" alt="Captura de pantalla 2022-11-22 a las 0 50 04" src="https://user-images.githubusercontent.com/47717915/203180985-a766cae0-f3c8-46a6-8f39-43d7fb0964dd.png">
