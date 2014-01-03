# -*- coding: utf-8 -*-

# Para poder interactua con HTTP
import urllib.parse as parser
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
    """
    url = httpget.urlopen(mainPageUrl)
    date = (re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).+",
                      re.search(filename + '.list.gz.{2,60}',
                                str(url.read())).group()).group()).rstrip()
    return date


def displayResults(searchResults):
    """
    Imprime la información de actor/actriz, peliculas, año, y rol
    """
    for i, j in searchResults.items():
        print("{}".format(i))
        for k in j:
            print("\t{}".format(k))
