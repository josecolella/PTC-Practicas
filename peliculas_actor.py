#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shelve
import os
from utilidades import displayResults
# Hacer una funcion que determine si un termino
# de busqueda se repite en la base de datos. Si se repite se devuelve
# las personas posibles. Determina el usuario final cual quiere
# Puedes recoger todas y preguntarle al usuario a quien se refiere


def search(personName):
    """
    Función creada para que se pueda buscar en la base de datos
    información relacionada con un actor
    """
    assert os.path.isfile("moviedb.bin"), "La base de datos no esta creada"
    db = shelve.open("moviedb.bin")
    person = {}
    try:
        person[personName] = db[personName]
    except KeyError:
        for key in db:
            if personName in key:
                person[key] = db[key]
    db.close()
    return person


if __name__ == '__main__':

    print("La actriz Kristen Hager")
    print("PERSON |--- FILM --- | --- YEAR --- | --- ROLE ---")
    displayResults(search("Kristen Hager"))

    print("La actriz George Clooney")
    print("PERSON |--- FILM --- | --- YEAR --- | --- ROLE ---")
    displayResults(search("George Clooney"))
