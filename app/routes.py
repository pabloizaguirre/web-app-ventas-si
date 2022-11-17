#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, database
from flask import render_template, request, url_for, redirect, session, jsonify, make_response
from app.busquedapelicula import filtrar_busqueda, filtrar_categoria
from app.compra import ejecutar_compra, introducir_saldo, precio_total_carrito, getHistorial, saldo_from_file
import json
import os
import sys
from collections import Counter
import random

catalogue = database.getCatalogue()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	# Creamos la lista con las categorias de peliculas
	categorias = database.getCategorias()
	catalogue = database.getCatalogue()

	if request.method == 'POST':
		if 'texto_busqueda' in request.form:
			filtracion = filtrar_busqueda(catalogue['peliculas'], request)
		if request.form['categorias'] != '':
			filtracion = filtrar_categoria(filtracion, request)

		return render_template('index.html', title = "Home", movies = filtracion, categorias=categorias)

	else:
		return render_template('index.html', title = "Home", movies=catalogue['peliculas'], categorias=categorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
	# doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
	if 'username' in request.form:
		try:
			customerid = database.comprobacionUsuario(request.form['username'], request.form['password'])
			session['usuario'] = customerid
			session.modified=True
			# se puede usar request.referrer para volver a la pagina desde la que se hizo login
			response = make_response(redirect(url_for('index')))
			response.set_cookie('lastUser', request.form['username'])
			return response
		except Exception as error:
			print(error)
			return render_template('login.html', title = "Sign In", mensaje_error=error)
	else:
		# se puede guardar la pagina desde la que se invoca 
		session['url_origen']=request.referrer
		session.modified=True        
		# print a error.log de Apache si se ejecuta bajo mod_wsgi
		print (request.referrer, file=sys.stderr)
		if 'lastUser' in request.cookies:
			print(request.cookies.get('lastUser'))
			return render_template('login.html', title = "Sign In", user = request.cookies.get('lastUser') )
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
			result = database.crearUsuario(request.form.to_dict())
			session['usuario'] = result
			return redirect(url_for('index'))

		except Exception as error:
			return render_template('registro.html', title = "Registro", mensaje_error=error)

	else:
		return render_template('registro.html', title = "Registro")    

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
	total = 0

	if 'carrito' in session:
		total = database.precio_total_carrito(session['carrito'], catalogue['peliculas'])

	return render_template('carrito.html', title = "Carrito", movies=catalogue['peliculas'], total=total)

@app.route('/historial', methods=['GET', 'POST'])
def historial():
	return render_template('historial.html', title="Historial de compras", historial=getHistorial(), movies=catalogue['peliculas'])

@app.route('/saldo', methods=['GET', 'POST'])
def saldo():
	if request.method == 'POST':
		database.introducir_saldo(float(request.form['saldo']))
		num_tarjeta = session['usuario']['creditcard']
		return render_template('saldo.html', title="Saldo", saldo=session['usuario']['saldo'], mensaje="Se ha hecho un cargo de " + request.form['saldo'] + "€ en la tarjeta: ************" + num_tarjeta[-5:-1])
	return render_template('saldo.html', title="Saldo", saldo=session['usuario']['saldo'])


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
	
	pelicula = database.getPelicula(id_pelicula)
	print(pelicula)
	if not pelicula:
		return redirect(url_for("index"))
	
	productos = database.getProductosPelicula(id_pelicula)

	return render_template('descripcion.html', title = pelicula['movietitle'], peli = pelicula, productos = productos)
	
""" Funciones AJAX """

@app.route('/_return_random_number', methods=['GET', 'POST'])
def return_random_number():
	return jsonify(result=random.randint(1000,2000))

@app.route('/_add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
	id_producto = request.args.get('prod_id', type=str)
	
	if 'usuario' not in session:
		if 'carrito' in session:
			session['carrito'][id_producto] += 1
			session.modified=True
		else:
			session['carrito'] = Counter([id_producto])
			session.modified=True
	else:
		database.addToCart(id_producto, session['usuario']['customerid'])
		
	return jsonify(result=1)

@app.route('/_remove_from_cart', methods=['GET', 'POST'])
def remove_from_cart():
	id_pelicula = request.args.get('film_id', type=str)

	if 'carrito' in session:
		if session['carrito'][id_pelicula] > 1:
			session['carrito'][id_pelicula] -= 1
			session.modified=True
		else:
			del session['carrito'][id_pelicula]
			session.modified=True
			if not session['carrito']:
				session.pop('carrito', None)
	else:
		session['carrito'] = Counter([id_pelicula])
		session.modified=True
	return jsonify(result=1)

@app.route('/_vaciar_carrito', methods=['GET', 'POST'])
def vaciar_carrito():
	session.pop('carrito', None)
	return jsonify(result=1)

@app.route('/_finalizar_compra', methods=['GET', 'POST'])
def finalizar_compra():
	if 'usuario' not in session:
		return jsonify(usuario=0, url=url_for('registro', necesario_registro=True))
	if not ejecutar_compra(session['carrito'], catalogue['peliculas'], app):
		return jsonify(usuario=1, suficiente_saldo=0)
	return jsonify(usuario=1, suficiente_saldo=1, url=url_for('carrito', mensaje_compra_confirmada=True))

@app.route('/_introducir_valoracion', methods=['GET', 'POST'])
def introducir_valoracion():
	valoracion = request.args.get('valoracion', type=int)
	id = request.args.get('film_id', type=str)

	if 'usuario' not in session:
		return jsonify(usuario=0)

	database.updateValoracion(id, valoracion, session['usuario']['customerid'])

	catalogue = database.getCatalogue()

	return jsonify(usuario=1,valorada=0)

@app.route('/_get_saldo', methods=['GET', 'POST'])
def get_saldo():
	return jsonify(result=session['usuario']['saldo'])
