# -*- coding: utf-8 -*-
import json
import random
from core import httptools
from core import scrapertools
from platformcode import platformtools, logger

def test_video_exists(page_url):
    types= "Archivo"
    gen = "o"
    msg = "El link tiene algún problema."
    id_video = None
    get = ""
    seqno = random.randint(0, 0xFFFFFFFF)
    url = page_url.split("#")[1]
    f_id = url.split("!")[1]
    id_video = None
    if "|" in url:
        url, id_video = url.split("|")
    post = {'a': 'g', 'g': 1, 'p': f_id}
    isfolder = False
    if "/#F!" in page_url:
        get = "&n=" + f_id
        post = {"a":"f","c":1,"r":0}
        isfolder = True
        types= "Carpeta"
        gen = "a"
        if id_video:
            #Aqui ya para hacer un check se complica, no hay una manera directa aún teniendo la id del video dentro de la carpeta
            return True, ""
            
    codes = {-1: 'Se ha producido un error interno en Mega.nz',
             -2: 'Error en la petición realizada, Cod -2',
             -3: 'Un atasco temporal o malfuncionamiento en el servidor de Mega impide que se proceso su link',
             -4: 'Ha excedido la cuota de transferencia permitida. Vuelva a intentarlo más tarde',
             -6: types + ' no encontrad' + gen + ', cuenta eliminada',
             -9: types + ' no encontrad'+ gen,
             -11: 'Acceso restringido',
             -13: 'Está intentando acceder a un archivo incompleto',
             -14: 'Una operación de desencriptado ha fallado',
             -15: 'Sesión de usuario expirada o invalida, logueese de nuevo',
             -16: types + ' no disponible, la cuenta del uploader fue baneada',
             -17: 'La petición sobrepasa su cuota de transferiencia permitida',
             -18: types + ' temporalmente no disponible, intentelo de nuevo más tarde'
    }
    api = 'https://g.api.mega.co.nz/cs?id=%d%s' % (seqno, get)
    req_api = httptools.downloadpage(api, json.dumps([post])).data
    if isfolder:
        req_api = json.loads(req_api)
    else:
        req_api = json.loads(req_api)[0]
    if isinstance(req_api, (int, long)):
        if req_api in codes:
            msg = codes[req_api]
        return False, msg
    else:
        return True, ""

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    from megaserver import Client
    c = Client(url=page_url, is_playing_fnc=platformtools.is_playing)
    files = c.get_files()

    # si hay mas de 5 archivos crea un playlist con todos
    # Esta función (la de la playlist) no va, hay que ojear megaserver/handler.py aunque la llamada este en client.py
    if len(files) > 5:
        media_url = c.get_play_list()
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [mega]", media_url])
    else:
        for f in files:
            media_url = f["url"]
            video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [mega]", media_url])

    return video_urls
