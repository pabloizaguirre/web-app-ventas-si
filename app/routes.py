#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, jsonify
from app.busquedapelicula import filtrar
from app.usuario import crearUsuario, comprobacionUsuario
import json
import os
import sys
from collections import Counter
import random

catalogue_data = open(os.path.join(app.root_path,'inventario/inventario.json'), encoding="utf-8").read()
catalogue = json.loads(catalogue_data)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        filtracion = filtrar(catalogue, request)
        return render_template('index.html', movies = filtracion)
    else:
        return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        # aqui se deberia validar con fichero .dat del usuario
        if request.form['username'] == 'pp':
            session['usuario'] = request.form['username']
            session.modified=True
            # se puede usar request.referrer para volver a la pagina desde la que se hizo login
            return redirect(url_for('index'))
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido
            return render_template('login.html', title = "Sign In")
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('usuario', None)
	session.pop('carrito', None)
	return redirect(url_for('index'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
	if request.method == 'POST':
		try: 
			crearUsuario(request.form["usuario"], request.form["clave"], request.form["correo"], request.form["tarjeta" ])
			return redirect(url_for('index'))

		except Exception as error:
			return redirect(url_for('registro'))

	else:
		return render_template('registro.html')    

@app.route('/indexregistrado', methods=['GET', 'POST'])
def indexregistrado():
    return render_template('indexregistrado.html')

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
	return render_template('carrito.html', movies=catalogue['peliculas'])

@app.route('/descripcion/<id_pelicula>', methods=['GET', 'POST'])
def descripcion(id_pelicula):

	if 'Add to cart' in request.args:
		if 'carrito' in session:
			session['carrito'][id_pelicula] += 1
			session.modified=True
		else:
			session['carrito'] = Counter([id_pelicula])
			session.modified=True

		return redirect(url_for('descripcion', id_pelicula=id_pelicula))
	
	listaPeliculas = catalogue["peliculas"]
	print(listaPeliculas)
	if not id_pelicula in listaPeliculas:
		return redirect(url_for("index"))
	
	
	return render_template('descripcion.html', peli = listaPeliculas[id_pelicula])
	
@app.route('/_return_random_number', methods=['GET', 'POST'])
def return_random_number():
	return jsonify(result=random.randint(1,10))
