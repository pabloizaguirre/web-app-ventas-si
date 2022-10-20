from flask import session
import os
import json

def precio_total_carrito(carrito, peliculas):
    total=0
    for id, num in carrito.items():
        total += peliculas[id]['precio'] * num
    return round(total,2)

def ejecutar_compra(carrito, peliculas, app):
    directorioU =  'si1users/' + session['usuario'] + '/userdata.dat'
    if not(os.path.exists(directorioU)):
        raise Exception("Nombre de usuario incorrecto")

    file = open(directorioU, 'r')

    content = file.readlines()

    file.close()
    
    if precio_total_carrito(carrito, peliculas) > float(content[4]):
        return False

    directorioC =  'si1users/' + session['usuario'] + '/compras.json'

    compras_file = open(directorioC, encoding="utf-8").read()
    if os.stat(directorioC).st_size == 0:
        compras = []
    else:
        compras = json.loads(compras_file)

    compra = []
    for id, num in carrito.items():
        compra.append({"id": id, "cantidad": num})

    compras.append(compra)

    # Actualizar el saldo
    content[4] = str(round(float(content[4]) - precio_total_carrito(carrito, peliculas), 2))

    a_file = open(directorioU, "w")
    a_file.writelines(content)
    a_file.close()

    with open(directorioC, 'w', encoding="utf-8") as catalogueFile:
        json.dump(compras, catalogueFile, indent=4)

    return True

def getHistorial():
    directorioC =  'si1users/' + session['usuario'] + '/compras.json'
    if os.stat(directorioC).st_size == 0:
        return []
    comprasData = open(directorioC, 'r', encoding="utf-8").read()
    compras = json.loads(comprasData)
    return compras


def saldo_from_file():
    directorioU =  'si1users/' + session['usuario'] + '/userdata.dat'
    if not(os.path.exists(directorioU)):
        raise Exception("Nombre de usuario incorrecto")

    file = open(directorioU, 'r')

    content = file.readlines()
    
    return float(content[4])

def introducir_saldo(cantidad):
    directorioU =  'si1users/' + session['usuario'] + '/userdata.dat'
    if not(os.path.exists(directorioU)):
        raise Exception("Nombre de usuario incorrecto")

    file = open(directorioU, 'r')

    content = file.readlines()

    content[4] = str(float(content[4]) + cantidad)

    file.close()

    a_file = open(directorioU, "w")
    a_file.writelines(content)
    a_file.close()

    return content[4]
