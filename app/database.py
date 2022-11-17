from collections import Counter
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

def addToCart(prod_id, customerid):
    # Comprobar si este customer tiene un order con status NULL
    db_conn = None
    db_conn = db_engine.connect()
    query = "select * from orders where customerid = " + str(customerid) + " and status is NULL"
    result = db_conn.execute(query).first()
    # Cuando no existe un carrito 
    if not result:
        # Conseguir el ultimo orderid
        query = "select * from orders order by orderid desc limit 1"
        result = db_conn.execute(query).first()
        if not result:
            orderid = 1
        else:
            orderid = result.orderid + 1
        
        query = "insert into orders (orderid, orderdate, customerid, netamount, tax, totalamount, status) values (" + str(orderid) + ", now(), " + str(customerid) + ", 0, 21, 0, NULL)"
        db_conn.execute(query)
    else:
        orderid = result.orderid
    
    # Comprobar que no hay un orderdetail con prod_id y orderid
    query = "select * from orderdetail where orderid = " + str(orderid) + " and prod_id = " + str(prod_id)
    result = db_conn.execute(query).first()
    if result:
        query = "update orderdetail set quantity = quantity + 1 where orderid = " + str(orderid) + " and prod_id = " + str(prod_id)
        db_conn.execute(query)
    else:
        query = "insert into orderdetail (orderid, prod_id, price, quantity) values (" + str(orderid) + ", " + str(prod_id) + ", (select price from products where prod_id = " + str(prod_id) + "), 1)"
        db_conn.execute(query)

    return

def removeFromCart(prod_id, customerid):
    db_conn = None
    db_conn = db_engine.connect()
    # Comprobar si hay un orderdetail con prod_id y orderid
    query = "select * from orderdetail natural join orders natural join customers where customerid=" + str(customerid) + "and prod_id=" + str(prod_id) + "and status is NULL"
    result = db_conn.execute(query).first()
    if result:
        query = "update orderdetail set quantity = quantity - 1 where orderid = " + str(result.orderid) + " and prod_id = " + str(prod_id)
        db_conn.execute(query)
        if result.quantity == 1:
            query = "delete from orderdetail where orderid = " + str(result.orderid) + " and prod_id = " + str(prod_id)
            db_conn.execute(query)
    return

def vaciarCarrito(customerid):
    db_conn = None
    db_conn = db_engine.connect()
    query = "delete from orderdetail where orderid in (select orderid from orders where customerid = " + str(customerid) + " and status is NULL)"
    db_conn.execute(query)
    return
    

def precioTotalCarrito(carrito): 
    if not carrito:
        return 0
    return sum([producto['orderprice'] * producto['quantity'] for producto in carrito])

def getCarrito():
    db_conn = None
    db_conn = db_engine.connect()
    if 'usuario' not in session:
        if 'carrito' in session:
            carrito = session['carrito']
        else:
            carrito = Counter()
        # Cogemos toda la informacion del carrito
        productos = []
        for prod_id, cantidad in carrito.items():
            query = "select price as orderprice, movietitle, movieid, description from products natural join imdb_movies where prod_id = " + str(prod_id)
            result = db_conn.execute(query).first()
            productos.append({'prod_id': prod_id, 'movietitle': result.movietitle, 'movieid': result.movieid, 'description': result.description, 'orderprice': result.orderprice, 'quantity': cantidad})
        return productos

    query = "select orderdetail.price as orderprice, quantity, movietitle, orderdetail.prod_id, movieid, description \
            from orderdetail \
                natural join orders \
                natural join customers \
                join products on products.prod_id=orderdetail.prod_id \
                natural join imdb_movies \
            where customerid=" + str(session['usuario']['customerid']) + " and status is NULL"
    result = db_conn.execute(query).all()
    if not result:
        return []
    carrito = []
    for producto in result:
        carrito.append(dict(producto))
    db_conn.close()
    return carrito

def introducirCarritoDB(carrito):
    for prod_id, cantidad in carrito.items():
        db_conn = None
        db_conn = db_engine.connect()
        # Obtener los orderdetail con prod_id y customerid=session['usuario']['customerid']
        query = "select * from orderdetail natural join orders natural join customers where customerid=" + str(session['usuario']['customerid']) + "and prod_id=" + str(prod_id) + "and status is NULL"
        result = db_conn.execute(query).first()
        if result:
            cantidad = max(cantidad, result.quantity)
            query = "update orderdetail set quantity =  " + str(cantidad) + " where orderid = " + str(result.orderid) + " and prod_id = " + str(prod_id)
            db_conn.execute(query)
        else:
            for _ in range(cantidad):
                addToCart(prod_id, session['usuario']['customerid'])
    return