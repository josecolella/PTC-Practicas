#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Jose Miguel Colella

import shelve
import os
from utilidades import displayResults, findPersonRegex
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
        person = findPersonRegex(db, personName)

    db.close()
    return person


if __name__ == '__main__':

    person1 = "Rachel Appleton"
    person2 = 'Kristen Hager'
    person3 = 'Seth Rogen'

    print("La actriz {}".format(person1))
    print("PERSON |--- FILM --- | --- YEAR --- | --- ROLE ---")
    displayResults(search(person1))

    print("La actriz {}".format(person2))
    print("PERSON |--- FILM --- | --- YEAR --- | --- ROLE ---")
    displayResults(search(person2))

    print("El actor {}".format(person3))
    print("PERSON |--- FILM --- | --- YEAR --- | --- ROLE ---")
    displayResults(search(person3))
