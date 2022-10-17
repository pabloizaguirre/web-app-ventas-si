#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, hashlib, random

def crearUsuario(form):

	if len(form['usuario']) == 0 or len(form['correo']) == 0 or len(form['clave']) == 0 or len(form['tarjeta']) == 0:
		raise Exception("Faltan campos")

	appDir = os.path.dirname(os.path.abspath(__file__))
	dirUsuario = os.path.join(appDir, '../si1users/' + form['usuario'])

	if os.path.exists(dirUsuario):
		raise Exception("Usuario ya existente")
	else:
		os.mkdir(dirUsuario)

	dir = os.path.join(dirUsuario, 'userdata.dat')
	dirCompras = os.path.join(dirUsuario, 'compras.json')

	file = open(dir, 'w')

	encriptado = hashlib.sha3_384()
	encriptado.update(form['clave'].encode('utf-8'))
	encriptado = encriptado.hexdigest()

	file.write(form['usuario'] + '\n')
	file.write(encriptado + '\n')
	file.write(form['correo'] + '\n')
	file.write(form['tarjeta'] + '\n')
	file.write(str(random.randint(0,50)))
	file.close()
	file = open(dirCompras, 'w')
	file.close()

def comprobacionUsuario(nombreUsuario, clave):
	if len(nombreUsuario) == 0 or len(clave) == 0:
		raise Exception("Error al comprobar la clave")
	
	directorioU =  'si1users/' + nombreUsuario + '/userdata.dat'
	
	if not(os.path.exists(directorioU)):
		raise Exception("Nombre de usuario incorrecto")

	file = open(directorioU, 'r')
	nUsuario = file.readline()[:-1]
	passw = file.readline()[:-1]

	encriptado = hashlib.sha3_384()
	encriptado.update(clave.encode('utf-8'))
	encriptado = encriptado.hexdigest()

	if nUsuario != nombreUsuario:
		file.close()
		raise Exception("El usuario no existe o no es correcto")

	if passw != encriptado:
		file.close()
		raise Exception("La clave no es correcta")

	file.close()