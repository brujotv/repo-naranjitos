# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
# deportesalacarta - XBMC Plugin
# Conector para dailymotion
# ---------------------------------------------------------------------------------------------------------------------

import re
from core import logger
from core import scrapertools

DEFAULT_HEADERS = [["User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"]]


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("pelisalacarta.servers.dailymotion get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data, headers = scrapertools.read_body_and_headers(page_url, headers=DEFAULT_HEADERS)
    data = data.replace("\\", "")
    '''
    "240":[{"type":"video/mp4","url":"http://www.dailymotion.com/cdn/H264-320x240/video/x33mvht.mp4?auth=1441130963-2562-u49z9kdc-84796332ccab3c7ce84e01c67a18b689"}]
    '''
    for cookie in headers:
        if cookie[0] == "set-cookie":
            header_cookie = cookie[1]
    DEFAULT_HEADERS.append(['Cookie', header_cookie])

    subtitle = scrapertools.find_single_match(data, '"subtitles":.*?"es":.*?urls":\["([^"]+)"')
    qualities = scrapertools.find_multiple_matches(data, '"([^"]+)":(\[\{"type":".*?\}\])')
    for calidad, urls in qualities:
        if calidad == "auto":
            continue
        patron = '"type":"(?:video|application)/([^"]+)","url":"([^"]+)"'
        matches = scrapertools.find_multiple_matches(urls, patron)
        for stream_type, stream_url in matches:
            stream_type = stream_type.replace('x-mpegURL', 'm3u8')
            if stream_type == "mp4":
                stream_url = scrapertools.get_header_from_response(stream_url, header_to_get="location",
                                                                   headers=DEFAULT_HEADERS)
            else:
                data_m3u8 = scrapertools.downloadpage(stream_url)
                stream_url = scrapertools.find_single_match(data_m3u8, '(http:.*?\.m3u8)')
            video_urls.append([calidad + "p ." + stream_type + " [dailymotion]", stream_url, 0, subtitle])

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.dailymotion %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.dailymotion.com/embed/video/xrva9o
    # http://www.dailymotion.com/swf/video/xocczx
    # http://www.dailymotion.com/swf/x17idxo&related=0
    # http://www.dailymotion.com/video/xrva9o
    patronvideos = 'dailymotion.com/(?:video/|swf/(?:video/|)|)(?:embed/video/|)(?!thumbnail)([A-z0-9]+)'
    logger.info("pelisalacarta.servers.dailymotion find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[dailymotion]"
        url = "http://www.dailymotion.com/embed/video/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'dailymotion'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
