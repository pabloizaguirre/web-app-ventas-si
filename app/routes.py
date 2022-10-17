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
		try:
			comprobacionUsuario(request.form['username'], request.form['password'])
			session['usuario'] = request.form['username']
			session.modified=True
			# se puede usar request.referrer para volver a la pagina desde la que se hizo login
			return redirect(url_for('index'))
		except Exception as error:
			return render_template('login.html', title = "Sign In", mensaje_error=error)
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
	session.pop('valoraciones', None)
	return redirect(url_for('index'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
	if request.method == 'POST':
		try: 
			crearUsuario(request.form.to_dict())
			session['usuario'] = request.form['usuario']
			return redirect(url_for('index'))

		except Exception as error:
			return render_template('registro.html', title = "Registro", mensaje_error=error)

	else:
		return render_template('registro.html', title = "Registro")    

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
	return render_template('carrito.html', movies=catalogue['peliculas'])

@app.route('/descripcion/<id_pelicula>', methods=['GET', 'POST'])
def descripcion(id_pelicula):

	if request.method == 'POST':
		print(request.form['options'])

	if 'Add to cart' in request.args:
		if 'carrito' in session:
			session['carrito'][id_pelicula] += 1
			session.modified=True
		else:
			session['carrito'] = Counter([id_pelicula])
			session.modified=True

		return redirect(url_for('descripcion', id_pelicula=id_pelicula))
	
	listaPeliculas = catalogue["peliculas"]
	if not id_pelicula in listaPeliculas:
		return redirect(url_for("index"))
	
	
	return render_template('descripcion.html', peli = listaPeliculas[id_pelicula])
	
""" Funciones AJAX """

@app.route('/_return_random_number', methods=['GET', 'POST'])
def return_random_number():
	return jsonify(result=random.randint(1000,2000))

@app.route('/_add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
	id_pelicula = request.args.get('film_id', type=str)

	if 'carrito' in session:
		session['carrito'][id_pelicula] += 1
		session.modified=True
	else:
		session['carrito'] = Counter([id_pelicula])
		session.modified=True
	return

@app.route('/_remove_from_cart', methods=['GET', 'POST'])
def remove_from_cart():
	id_pelicula = request.args.get('film_id', type=str)

	if 'carrito' in session:
		if session['carrito'][id_pelicula] > 0:
			session['carrito'][id_pelicula] -= 1
			session.modified=True
		else:
			del session['carrito'][id_pelicula]
	else:
		session['carrito'] = Counter([id_pelicula])
		session.modified=True
	return

@app.route('/_vaciar_carrito', methods=['GET', 'POST'])
def vaciar_carrito():
	session.pop('carrito', None)
	return

@app.route('/_introducir_valoracion', methods=['GET', 'POST'])
def introducir_valoracion():
	valoracion = request.args.get('valoracion', type=int)
	id = request.args.get('film_id', type=str)

	if('valoraciones' not in session):
		session['valoraciones'] = [id]
	elif(id in session['valoraciones']):
		return jsonify(valorada=1)
	else:
		session['valoraciones'].append(id)

	valoracion_antigua = catalogue['peliculas'][id]['valoracion']
	num_val = catalogue['peliculas'][id]['numeroValoraciones']
	nueva_valoracion = (valoracion_antigua*num_val + valoracion)/(num_val + 1)

	catalogue['peliculas'][id]['valoracion'] = nueva_valoracion
	catalogue['peliculas'][id]['numeroValoraciones'] = num_val + 1

	with open(os.path.join(app.root_path,'inventario/inventario.json'), 'w', encoding="utf-8") as catalogueFile:
		json.dump(catalogue, catalogueFile, indent=4)

	return jsonify(valorada=0)