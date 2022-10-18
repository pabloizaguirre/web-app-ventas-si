#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request

def filtrar_busqueda(listapeliculas, request):
	listado = {}
	
	seleccionado = request.form['texto_busqueda'].lower()
	if len(seleccionado) != 0 and seleccionado != "":
		listaAux = listapeliculas["peliculas"]
		for id, pelicula in listaAux.items():
			titulo = pelicula["titulo"].lower()
			if titulo.find(seleccionado) != -1:
				listado[id] = pelicula
		return listado

	else:
		return listapeliculas['peliculas']

def filtrar_categoria(listaPeliculas, request):
	listado = {}
	categoria = request.form['categorias']
	for id, pelicula in listaPeliculas['peliculas'].items():
		if pelicula['categoria'] == categoria:
			listado[id] = pelicula
	
	return listado
