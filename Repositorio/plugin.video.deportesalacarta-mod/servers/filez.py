# -*- coding: utf-8 -*-
#------------------------------------------------------------
# deportesalacarta - XBMC Plugin
# Conector para filez
#------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url, follow_redirects=False)

    if data.headers.get("location"):
        return False, "[filez] El archivo ha sido eliminado o no existe"
    
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    
    data = httptools.downloadpage(page_url).data

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)",\s*type\s*:\s*"([^"]+)"')
    for media_url, ext in media_urls:
        video_urls.append([".%s [filez]" % ext, media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = 'filez.tv/(?:embed/u=|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filez]"
        url = "http://filez.tv/embed/u=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filez'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
