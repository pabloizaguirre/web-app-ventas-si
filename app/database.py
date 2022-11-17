import random
from sqlalchemy import create_engine, MetaData
import os
from flask import session

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

def introducir_saldo(cantidad):
    db_conn = None
    db_conn = db_engine.connect()
    query = "UPDATE public.customers SET balance = balance + " + str(cantidad) + " WHERE customerid = " + str(session['usuario']['customerid'])
    db_conn.execute(query)
    db_conn.close()
    session['usuario']['saldo'] += cantidad
    return 

# return the 10 most popular movies
def getCatalogue():
    db_conn = None
    db_conn = db_engine.connect()
    query = "select * from imdb_movies \
            natural join (select movieid, SUM(sales) as sales from products group by movieid) as allsales \
            order by sales desc \
            limit 10"
    
    result = db_conn.execute(query).all()

    catalogue = {"peliculas": dict(zip([film.movieid for film in result], [dict(film) for film in result]))}

    return catalogue

# Obtener todas las categorias de la tabla genres
def getCategorias():
    db_conn = None
    db_conn = db_engine.connect()
    query = "select * from genres"
    categorias = []
    for categoria in db_conn.execute(query).all():
        categorias.append(categoria.genre)
    db_conn.close()
    return categorias

def getPelicula(id):
    db_conn = None
    db_conn = db_engine.connect()
    query = "select * from imdb_movies where movieid = " + str(id)
    result = db_conn.execute(query).first()
    db_conn.close()
    return dict(result)

def updateValoracion(movieid, valoracion, customerid):
    db_conn = None
    db_conn = db_engine.connect()
    query = "select * from ratings where customerid = " + str(customerid) + " and movieid = " + str(movieid)
    result = db_conn.execute(query).first()
    if result:
        query = "update ratings set rating = " + str(valoracion) + " where customerid = " + str(customerid) + " and movieid = " + str(movieid)
    else:
        query = "insert into ratings (customerid, movieid, rating) values (" + str(customerid) + ", " + str(movieid) + ", " + str(valoracion) + ")"
    db_conn.execute(query)
    db_conn.close()
    return

# Obtener todos los productos de la tabla products con un determinado movieid
def getProductosPelicula(movieid):
    db_conn = None
    db_conn = db_engine.connect()
    query = "select * from products where movieid = " + str(movieid)
    productos = []
    for producto in db_conn.execute(query).all():
        productos.append(dict(producto))
    db_conn.close()
    return productos

# Obtener el precio total del carrito

def addToCart(prod_id, customerid):
    return