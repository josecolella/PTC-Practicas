#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Jose Miguel Colella

import shelve


def find_shortest_path(graph, start, end, path=[]):
    """
    Conseguir el camino más corto. Este algoritmo esta implementado
    en los tutoriales de python sobre los gráfos.

    http://www.python.org/doc/essays/graphs/
    @return tuple Tupla con el primer parametro que es la lista de relaciones
    de una persona a otra
    """
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def getActorsWorkedWith(person):
    """
    Devuelve un diccionario que contiene los actores/actrices de los
    cuales ha trabajado un actor

    @return dict Diccionario con los actores/actrices con los cuales
    ha trabajado en actor/actriz
    """
    try:
        moviedb = shelve.open('degree.bin')
        db = shelve.open('moviedb.bin')
        actorsWorkedWith = []
        for i in db[person]:
            filmNameYear = '{} {}'.format(i[0], i[1])
            if filmNameYear in moviedb:
                for j in moviedb[filmNameYear]:
                    if j != person:
                        actorsWorkedWith.append(j)
            else:
                print("NO")
        db.close()
        moviedb.close()
        return actorsWorkedWith
    except KeyError:
        print("La persona no esta en la base de datos")


def degreeSeparation(person1, person2):
    """
    Consigue el grado de separacion entre dos actores/ actrices.
    Dicha relación se establece directamente o indirectemente mediante
    relaciones con otros actores/actrices.

    @return tuple Tupla con el primer parametro siendo una lista
    de relaciones de la primera persona a la segunda. El segundo parametro
    es un entero que representa el número de grados
    """
    person1ActorsWorkedWith = {person1: getActorsWorkedWith(person1)}
    person1Copy = person1ActorsWorkedWith.copy()
    for j in person1ActorsWorkedWith[person1]:
        if j not in person1Copy:
            person1Copy[j] = getActorsWorkedWith(j)
    person1ActorsWorkedWith = person1Copy
    del person1Copy
    shortestPath = find_shortest_path(
        person1ActorsWorkedWith, person1, person2)
    try:
        return shortestPath, len(shortestPath) - 1
    except TypeError:
        print("No hay camino entre {} y {}".format(person1, person2))

if __name__ == '__main__':

    # Las personas a buscar
    person1 = 'Rachel Appleton'
    person2 = "Kristen Hager"
    shortestPath, length = degreeSeparation(person1, person2)
    print("Camino entre {} y {}".format(person1, person2))
    print("El camino más corto es: {}".format(shortestPath))
    print("El grado de separación es: {}".format(length))
