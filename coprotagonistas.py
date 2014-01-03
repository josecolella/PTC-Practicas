#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peliculas_actor import search


def getRelationalMovies(person1, person2):
    """
    Esta función devuelve las peliculas en las cuales
    las personas que se pasan por parametros han sido protagonistas

    @return list Una lista de peliculas en las cual son coprotagonistas
    """
    person1Movies = (search(person1)).values()
    person2Movies = (search(person2)).values()
    person1Movies = [[(i[0], i[1]) for i in j] for j in person1Movies]
    person2Movies = [[(i[0], i[1]) for i in j] for j in person2Movies]
    person1Movies = person1Movies[0]
    person2Movies = person2Movies[0]
    commonFilms = list(
        filter((lambda i: i in person1Movies and i in person2Movies),
               person1Movies))
    return commonFilms

if __name__ == '__main__':

    print(getRelationalMovies('George Clooney', 'Matt Damon'))
