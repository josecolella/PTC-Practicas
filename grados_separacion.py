#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Jose Miguel Colella

import shelve


def bfs(graph, start, end):
    """
    Devuelve el camino que denota una busqueda de breadth first
    search desde <start> a <end>

    @param start Comienzo de la busqueda
    @param end Nodo final
    @return list Camino desde start a end
    """
    bfs = []
    bfs.append([start])
    while bfs:
        path = bfs.pop(0)
        node = path[-1]
        if node == end:
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            bfs.append(new_path)
    return bfs


def degreeSeparation(person1, person2):
    """
    Consigue el grado de separacion entre dos actores/ actrices.
    Dicha relación se establece directamente o indirectemente mediante
    relaciones con otros actores/actrices.

    @return tuple Tupla con el primer parametro siendo una lista
    de relaciones de la primera persona a la segunda. El segundo parametro
    es un entero que representa el número de grados
    """
    db = shelve.open('degree.bin')
    shortestPath = bfs(db, person1, person2) if len(
        db[person1]) < len(db[person2]) else bfs(db, person2, person1)
    try:
        return shortestPath, len(shortestPath) - 1
    except TypeError:
        print("No hay camino entre {} y {}".format(person1, person2))
    db.close()

if __name__ == '__main__':

    # Las personas a buscar
    person1 = 'Kristen Hager'
    person2 = 'Rachel Appleton'
    shortestPath, length = degreeSeparation(person1, person2)
    print("Camino entre {} y {}".format(person1, person2))
    print("El camino más corto es: {}".format(shortestPath))
    print("El grado de separación es: {}".format(length))
