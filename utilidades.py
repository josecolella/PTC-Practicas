# -*- coding: utf-8 -*-
# Author: Jose Miguel Colella

# Para poder interactuar con HTTP
import urllib.parse as parser  # Parser de url -> Tiempo de modificación
import urllib.request as httpget
import re

# Enlaces a las páginas
actressListUrl = "ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz"
actorsListUrl = "ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz"
mainPageUrl = "ftp://ftp.fu-berlin.de/pub/misc/movies/database/"


def getFilenameUrl(urlToParse):
    """
    Función que devuelve el nombre
    de un fichero que hace parte de
    la url que se pasa como parametro

    @param urlToParse url a parsear
    @return str Nombre del fichero

    """
    url = parser.urlparse(urlToParse)
    pathToFile = url.path
    fileName = re.search(
        r'\w+.list.gz', pathToFile, re.IGNORECASE).group()
    fileNameNoExt = re.sub(".list.gz", "", fileName)
    return fileName, fileNameNoExt


def getFileModDate(urlToParse, filename):
    """
    Devuelve la fecha de modificación del fichero que se pasa
    por parametro

    @param urlToParse La url que se parsea
    @param filename El nombre del fichero que se busca la fecha de modificación
    @return str Última fecha de modificación
    """
    url = httpget.urlopen(mainPageUrl)
    date = (re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+",
                      re.search(filename + '.list.gz.{2,60}',
                                str(url.read())).group()).group()).rstrip()
    return date


def mergeDictionary(dict1, dict2):
    """
    Devuelve un diccionario que esta compuesto de los dos diccionarios
    que se pasan como parametro. Esto significa que si hay una llave
    que existe en los dos diccionarios, el nuevo diccionario tendra
    la agregacion de los valores de dicha llave

    @param dict1 primer diccionario
    @param dict2 segundo diccionario
    @return dict
    """
    mergedDict = {}
    for i, j in zip(dict1, dict2):
        if i not in mergedDict:
            mergedDict[i] = set()
        if j not in mergedDict:
            mergedDict[j] = set()
        mergedDict[i].update(dict1[i])
        mergedDict[j].update(dict2[j])
    return mergedDict


def displayResults(searchResults):
    """
    Imprime la información de actor/actriz, peliculas, año, y rol
    """
    try:
        for i, j in searchResults.items():
            print("{}".format(i))
            for k in j:
                print("\t{}".format(k))
    except Exception:
        for i in searchResults:
            print("\t{}".format(i))


def findPersonRegex(db, personName):
    # Si no se consigue persona
    possibleDict = {}
    actorRegex = re.compile(personName + '\s*(\(.*?\))?')
    print("Mutiples personas con nombre: {}".format(personName))
    possiblePeopleList = list(
        filter(lambda i: re.search(actorRegex, i), db.keys()))
    if len(possiblePeopleList) > 0:
        for possiblePeople in possiblePeopleList:
            possibleDict[possiblePeople] = db[possiblePeople]
    return possibleDict
