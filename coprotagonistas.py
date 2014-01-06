#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: Jose Miguel Colella

import shelve
import os.path


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
        person2Movies = db[person2]
    except KeyError:
        for key in db:
            if person1 in key:
                person1Movies = db[key]
            if person2 in key:
                person2Movies = db[key]

    db.close()
    person1Movies = [(i[0], i[1]) for i in person1Movies]
    person2Movies = [(i[0], i[1]) for i in person2Movies]
    commonFilms = list(
        filter((lambda i: i in person1Movies and i in person2Movies),
               person1Movies))
    return commonFilms

if __name__ == '__main__':

    person1 = 'Angelina Jolie'
    person2 = 'Kristen Hager'
    print("Peliculas entre: {} y {}".format(person1, person2))
    print(getRelationalMovies(person1, person2))
    person2 = 'Rachel Appleton'
    print("Peliculas entre: {} y {}".format(person1, person2))
    print(getRelationalMovies(person1, person2))
