import random
from sqlalchemy import create_engine, MetaData
import os

db_engine = create_engine('postgresql://alumnodb:@localhost:5432/si1', echo=False)
db_meta = MetaData(bind=db_engine)

def get_movie(movieid):
    db_conn = None
    db_conn = db_engine.connect()
    query = "SELECT * FROM public.imdb_movies WHERE movieid = " +  str(movieid)
    result = db_conn.execute(query).all()
    db_conn.close()
    return result

def comprobacionUsuario(username, password):
    db_conn = None
    db_conn = db_engine.connect()
    query = "SELECT * FROM public.customers WHERE username = '" +  str(username) + "' AND password = '" + str(password) + "'"
    result = db_conn.execute(query).first()
    db_conn.close()
    if not result:
        raise Exception("Usuario o contraseña incorrectos")
    keys = ["customerid", "address", "email", "creditcard", "username", "password", "saldo"]
    return dict(zip(keys, list(result)))

def usuarioEnBD(username):
    db_conn = None
    db_conn = db_engine.connect()
    query = "SELECT * FROM public.customers WHERE username = '" +  str(username) + "'"
    result = db_conn.execute(query).first()
    db_conn.close()
    if not result:
        return False
    return True

def correoEnBD(correo):
    db_conn = None
    db_conn = db_engine.connect()
    query = "SELECT * FROM public.customers WHERE email = '" +  str(correo) + "'"
    result = db_conn.execute(query).first()
    db_conn.close()
    if not result:
        return False
    return True

def crearUsuario(form):
    if len(form['usuario']) == 0 or len(form['correo']) == 0 or len(form['clave']) == 0 or len(form['tarjeta']) == 0:
        raise Exception("Faltan campos")
    
    if usuarioEnBD(form['usuario']):
        raise Exception("El usuario ya existe")

    if correoEnBD(form['correo']):
        raise Exception("Este correo ya esta registrado")

    try:
        db_conn = None
        db_conn = db_engine.connect()
        
        result = db_conn.execute("SELECT COUNT(*) FROM public.customers")
        customerid = result.all()[0].count + 1

        db_conn.execute("INSERT INTO public.customers (customerid, address, email, creditcard, username, password, balance ) \
                        VALUES (" + str(customerid) + ", '" + form['direccion'] + "', '" + form['correo'] + "', '" + \
                        form['tarjeta'] + "', '" + form['usuario'] + "', '" + form['clave'] + "', " + str(random.randint(0,50)) + ")")

        result = db_conn.execute("SELECT * FROM public.customers WHERE customerid='" + str(customerid) + "'").first()

        db_conn.close()
        
        keys = ["customerid", "address", "email", "creditcard", "username", "password", "saldo"]
        return dict(zip(keys, list(result)))
    
    except Exception as e:
        print(e)
        raise Exception("Error al crear el usuario")

