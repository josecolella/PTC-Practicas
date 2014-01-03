#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ejecutando el programa aproximadamente 30 minutos con algoritmos
# cuya complejidad maxima es O(n)

import urllib.request
import gzip  # Para trabajar con gzip
from utilidades import *
import os.path
import shelve  # Para guardar información sobre fecha de modificación
import re
import codecs


def downloadFile(url, filename):
    """
    Función usada para descargar la <url>
    pasada por parametro. Todo el
    contenido estará guardado en el filename
    que se pasa como parametro.

    Además que se guarda información sobre la fecha de modificación
    con shelve usando la información que proporciona la url
    principal.

    @return bool Si el fichero ha sido modificado
    """

    f = urllib.request.urlopen(url)
    # Archivo que contiene información sobre fecha modificación
    fmod = shelve.open('modDate.bin')
    filename, fileNameNoExt = getFilenameUrl(url)
    # Consigue fecha de modificación
    modDate = getFileModDate(mainPageUrl, fileNameNoExt)
    # Si el fichero no existe o la fecha de modificación no es igual a la
    # que esta guardada, se graba el fichero en disco
    if not os.path.isfile(filename) or modDate != fmod[fileNameNoExt + '-last-mod']:
        isChanged = True
        fmod[fileNameNoExt + '-last-mod'] = getFileModDate(
            mainPageUrl, fileNameNoExt)
        urllib.request.urlretrieve(url, filename)
    else:
        isChanged = False
        print(
            "No hay cambio en {} y no se ha descargado".format(filename))
    f.close()
    fmod.close()

    return isChanged


def saveDatabase(filename, database):
    """
    Esta función sirve para guardar información
    sobre un actor ó actriz, en el cual tenemos
    el nombre de dicho actor o actriz como valor
    llave y tenemos las peliculas, la fecha y el papel.
    El parametro de entrada tiene que ser de tipo diccionario

    Complejidad: O(n)
    """
    assert type(database) == dict, 'El parametro tiene que ser un diccionario'
    assert type(
        filename) == str, 'El primer parametro tiene que ser una cadena de caracteres'
    db = shelve.open(filename)
    # Guardar el diccionario en disco
    db.update(database)
    db.close()


def processFile(file):
    """
    processFile(file) toma un fichero como parametro y procesa dicho fichero
    Devuelve un diccionario con el nombre del actor/actriz como llave y
    las peliculas, años, y roles como valor

    @param file Fichero a procesar
    @return dict Diccionario con la información de los actores
    """
    assert type(
        file) == str, 'El parametro tiene que ser una cadena de caracteres'
    # Las expresiones regulares usadas
    movieRegex = re.compile(
        '\s+([\d?\D]+).\(([0-9?]+)(?:/\w+)?\)(?:[^[]+)?\[?([^\]]+)?')
    actorFirstMovieRegex = re.compile(
        '^([a-zA-Z.? ?]+),(.\w{4,})\s*(\(.*?\))?([\d?\D]+).\(([0-9?]+)(?:/\w+)?\)(?:[^[]+)?\[?([^\]]+)?')

    f = codecs.iterdecode(gzip.open(file), 'latin-1')

    db = {}
    moviedb = {}
    for i in f:
        # Actor plus first movie
        match = re.search(actorFirstMovieRegex, i)
        moviesInfo = []
        # Se ha visto un actor/actriz con la primera pelicula
        if match:
            firstName = match.group(2)
            lastName = match.group(1)
            optionalField = match.group(
                3) if match.group(3) is not None else ''
            if optionalField is None:
                act = (firstName + " " + lastName).strip()
            else:
                act = (
                    firstName + " " + lastName + " " + optionalField).strip()
            db[act] = []  # Empty list
            filmName = match.group(4)
            filmYear = match.group(5)
            filmRole = match.group(6)
            filmName = (filmName.strip()).strip(
                "\"") if filmName is not None else ''
            filmYear = filmYear.strip(
                "()") if filmYear is not None else ''
            filmNameYear = filmName + " " + filmYear
            if filmNameYear not in moviedb:
                moviedb[filmNameYear] = []
            filmRole = filmRole.strip(
                "[""]") if filmRole is not None else ''
            if act not in moviedb[filmNameYear]:
                moviedb[filmNameYear].append(act)
        else:
            # Se ha visto una pelicula
            match = re.search(movieRegex, i)
            if match:
                filmName = match.group(1)
                filmYear = match.group(2)
                filmRole = match.group(3)
                filmName = (filmName.strip()).strip(
                    "\"") if filmName is not None else ''
                filmYear = filmYear.strip(
                    "()") if filmYear is not None else ''
                filmNameYear = filmName + " " + filmYear
                if filmNameYear not in moviedb:
                    moviedb[filmNameYear] = []
                filmRole = filmRole.strip(
                    "[""]") if filmRole is not None else ''
                try:
                    if act not in moviedb[filmNameYear]:
                        moviedb[filmNameYear].append(act)
                except UnboundLocalError:
                    pass
        # Si se ha encontrado una match
        if match:
            try:
                moviesInfo.extend([filmName, filmYear, filmRole])
                db[act].append(moviesInfo)
            except UnboundLocalError:
                # Si no estan asignadas
                pass
    f.close()
    return db, moviedb


if __name__ == '__main__':

    # Descarga lista de actrices
    normalActress = getFilenameUrl(actressListUrl)[0]
    # Descarga del fichero de las actrices
    hasChangedActressFile = downloadFile(actressListUrl, normalActress)

    # Procesamiento de información
    if hasChangedActressFile:
        actressdb, actressMovieDB = processFile(normalActress)
        saveDatabase('moviedb.bin', actressdb)
        print("Las actrices han sido grabada")
        saveDatabase('degree.bin', actressMovieDB)
        print("Las peliculas de las actrices han sido grabadas")
    else:
        print("La información de las actrices ya esta en las bases de datos")

    # Descargar lista de actores
    normalActor = getFilenameUrl(actorsListUrl)[0]
    # Descarga lista de actores
    hasChangedActorFile = downloadFile(actorsListUrl, normalActor)

    # Procesamiento de información
    if hasChangedActorFile:
        actordb, actorMovieDB = processFile(normalActor)
        saveDatabase('moviedb.bin', actordb)
        print("Los actores han sido grabada")
        saveDatabase('degree.bin', actorMovieDB)
        print("Las peliculas de los actores han sido grabadas")
    else:
        print("La información de los actores ya esta en las bases de datos")
