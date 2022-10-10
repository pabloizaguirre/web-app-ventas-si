#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, hashlib, random

def crearUsuario(nombreUsuario, clave, email, tarjeta):
	if len(nombreUsuario) == 0 or len(email) == 0 or len(clave) == 0 or len(tarjeta) == 0:
		raise Exception("Faltan campos")

	dirUsuario = 'si1users/' + nombreUsuario

	if os.path.exists(dirUsuario):
		raise Exception("usuario ya existente")
	else:
		os.mkdir(dirUsuario)

	dir = os.path.join(dirUsuario, 'userdata.dat')
	dirCompras = os.path.join(dirUsuario, 'compras.json')

	file = open(dir, 'w')

	encriptado = hashlib.sha3_384()
	encriptado.update(clave.encode('utf-8'))
	encriptado.hexdigest()

	file.write(nombreUsuario + '\n')
	file.write(encriptado + '\n')
	file.write(email + '\n')
	file.write(tarjeta + '\n')
	file.write(str(random.randint(0,500)))
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
	nUsuario = file.readline()
	passw = file.readline()

	encriptado = hashlib.sha3_384()
	encriptado.update(clave.encode('utf-8'))
	encriptado.hexdigest()

	if nUsuario != nombreUsuario:
		file.close()
		raise Exception("El usuario no existe o no es correcto")

	if passw != encriptado:
		file.close()
		raise Exception("La clave no es correcta")

	file.close()