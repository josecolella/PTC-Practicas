#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Jose Miguel Colella

import shelve
import os.path
from utilidades import findPersonRegex, displayResults


def getRelationalMovies(person1, person2):
    """
    Esta función devuelve las peliculas en las cuales
    las personas que se pasan por parametros han sido protagonistas

    @return list Una lista de peliculas en las cual son coprotagonistas
    """
    assert os.path.isfile("moviedb.bin"), "La base de datos no esta creada"
    db = shelve.open("moviedb.bin")
    try:
        person1Movies = db[person1]
    except KeyError:
        person1Movies = findPersonRegex(db, person1)
    try:
        person2Movies = db[person2]
    except KeyError:
        person2Movies = findPersonRegex(db, person2)

    db.close()
    person1Movies = [(i[0], i[1]) for i in person1Movies]
    person2Movies = [(i[0], i[1]) for i in person2Movies]
    commonFilms = list(
        filter((lambda i: i in person1Movies and i in person2Movies),
               person1Movies))
    return commonFilms

if __name__ == '__main__':

    person2 = 'Rachel Appleton'
    person1 = 'Carl Chase (I)'
    print("Peliculas entre: {} y {}".format(person1, person2))
    displayResults(getRelationalMovies(person1, person2))
    # person2 = 'Zachary Quinto'
    # print("Peliculas entre: {} y {}".format(person1, person2))
    # displayResults(getRelationalMovies(person1, person2))
