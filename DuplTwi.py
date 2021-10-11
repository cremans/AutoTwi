import requests
import urllib.parse
import m3u8
import os
import math


url_api = "https://gql.twitch.tv/gql"

cabecera_token = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES',
            'Authorization': 'undefined',
            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Connection': 'keep-alive',
            'Content-Length': '662',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Device-Id': '0xuvWh0J2XUXQo78MMqtsAdD4xGPZ1ON',
            'Host': 'gql.twitch.tv',
            'Origin': 'https://www.twitch.tv',
            'Referer': 'https://www.twitch.tv/',
            'sec-ch-ua': '"Chromium";v="93", " Not A;Brand";v="99", "Google Chrome";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.131 Safari/537.36'
            }

cabecera_m3u8 = {
            'Accept': 'application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.131 Safari/537.36'
            }

cabecera_data = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES',
            'Authorization': 'undefined',
            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Connection': 'keep-alive',
            'Content-Length': '287',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Device-Id': '0xuvWh0J2XUXQo78MMqtsAdD4xGPZ1ON',
            'Host': 'gql.twitch.tv',
            'Origin': 'https://www.twitch.tv',
            'Referer': 'https://www.twitch.tv/',
            'sec-ch-ua': '"Chromium";v="93", " Not A;Brand";v="99", "Google Chrome";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.131 Safari/537.36'
            }

lst_nomSim = {
    '|': '.l.',
    '>': '.M.',
    '<': '.m.',
    '"': '.__.',
    '?':  '.!.',
    '*': '.x.',
    ':': '.-.',
    '/': '.).',
    '\\': '.(.',
    }


def solicitarToken(vodID):
    global url_api
    global cabecera_token

    bdy_token = [
        {
            'operationName':'PlaybackAccessToken_Template',
            'query': 'query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: '
                     'Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: '
                     '{platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) '
                     '@include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken'
                     '(id: $vodID, params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: '
                     '$playerType}) @include(if: $isVod) {    value    signature    __typename  }}',
            'variables':{
                'isLive':False,
                'login':'',
                'isVod': True,
                'vodID': vodID,
                'playerType': 'site'
            }
        }
    ]

    respuesta_token = requests.post(url_api, json=bdy_token, headers=cabecera_token)
    contenido_token = respuesta_token.json()

    firma = contenido_token[0]['data']['videoPlaybackAccessToken']['signature']
    token = contenido_token[0]['data']['videoPlaybackAccessToken']['value']
    token_cod = urllib.parse.quote(token, safe='')

    return firma, token_cod


def obtenerReso(vodID, firma, token_cod):
    global cabecera_m3u8
    
    url_reso = 'https://usher.ttvnw.net/vod/' + vodID + '.m3u8?allow_source=true& player_backend=mediaplayer&' \
               'playlist_include_framerate=true&reassignments_supported=true&sig=' + firma + '&supported_codecs=' \
               'avc1&token=' + token_cod + '&cdm=wv&player_version=1.5.0'

    arch_reso = requests.get(url_reso, headers=cabecera_m3u8)

    m3u8_reso = m3u8.loads(arch_reso.text)

    return m3u8_reso.data['playlists'][0]['uri']


def obtenerFrag(url_frag):
    global cabecera_m3u8

    arch_frag = requests.get(url_frag, headers=cabecera_m3u8)

    m3u8_frag = m3u8.loads(arch_frag.text)

    return m3u8_frag.data['segments']


def obtenerNom(vodID):
    global url_api
    global cabecera_data
    
    bdy_data = [
        {
            'operationName':'ComscoreStreamingQuery',
            'variables':{
                'channel':'',
                'clipSlug':'',
                'isClip': False,
		'isLive': False,
		'isVodOrCollection':  True,
                'vodID': vodID,
            },
	    'extensions': {
		    'persistedQuery': {
			    'version': 1,
			    'sha256Hash': 'e1edae8122517d013405f237ffcc124515dc6ded82480a88daef69c83b53ac01'
			}
		}
        }
    ]

    respuesta_data = requests.post(url_api, json=bdy_data, headers=cabecera_data)
    data = respuesta_data.json()

    return data[0]['data']['video']['title']


def main(vodID):
    global lst_nomSim
    
    nom_orig = obtenerNom(vodID)
    os.system("echo Nombre Original: " + nom_orig)
    nom_modf = nom_orig
    for simbolo in lst_nomSim:
        nom_modf = nom_modf.replace(simbolo, lst_nomSim[simbolo])
    os.system("echo Nombre Modificado:  " + nom_modf)
    
    firma, token_cod = solicitarToken(vodID)
    url_frag = obtenerReso(vodID, firma, token_cod)
    lista_frag = obtenerFrag(url_frag)

    url_ts = url_frag[:len(url_frag)- url_frag[::-1].index('/')]
    os.system("echo -------------------------------------------------")
    os.system("echo URL HLS Fragmentos: " + url_frag)
    os.system("echo URL HLS Base TS: " + url_ts)

    if len(nom_modf + ".mp4") > 203:
        nom_vid = nom_modf[:203] + " [...]"
    else:
        nom_vid = nom_modf
    print("\n-------------------------------------------------")
    print("Nombre de archivo recortado: \n")
    print(nom_vid)

    print("\n-------------------------------------------------")
    print("Descarga de Fragmentos. Errores:")
    with open(nom_vid + ".ts", "wb") as arch_ts:
        for item in lista_frag:
            respuesta = requests.get(url_ts + item['uri'])
            if respuesta.status_code == 200:
                arch_ts.write(respuesta.content)
            else:
                print("Fragmento " + item['uri'] + " - Codigo de error <" + str(respuesta.status_code) + ">")

    print("\n-------------------------------------------------")
    print("Ejecutando ffmpeg.exe")
    print("Comando:")
    print('ffmpeg.exe -y -i "' + nom_vid + '.ts" -c:v copy -c:a copy "' + nom_vid + '.mp4"')
    os.system('ffmpeg.exe -y -i "' + nom_vid + '.ts" -c:v copy -c:a copy "' + nom_vid + '.mp4"')
    print("\n-------------------------------------------------")
    print("Eliminando archivo TS")
    os.remove(nom_vid + '.ts')

    peso_arch = os.stat(nom_vid + '.mp4').st_size
    peso_arch = peso_arch/1024/1024/1024
    print("\n-------------------------------------------------")
    print("Peso del archivo: %.2f GB" %peso_arch)

    print("\n-------------------------------------------------")
    print("Comprimiendo archivo MP4. Ejecutando winrar.exe")
    print("Comando:")
    if peso_arch <= 14:
        print('winrar.exe a -afrar -df -m5 -mt3 -ri15 -t -tk -ts "' + nom_vid + '.rar" "' + nom_vid + '.mp4"')
        os.system('winrar.exe a -afrar -df -m5 -mt3 -ri15 -t -tk -ts "' + nom_vid + '.rar" "' + nom_vid + '.mp4"')
    elif peso_arch > 14 and peso_arch <= 28:
        tam_vol = math.ceil(peso_arch/2)
        print('winrar.exe a -afrar -df -m5 -mt3 -ri15 -t -tk -ts -v' + str(tam_vol) + 'g "' + nom_vid +
              '.rar" "' + nom_vid + '.mp4"')
        os.system('winrar.exe a -afrar -df -m5 -mt3 -ri15 -t -tk -ts -v' + str(tam_vol) + 'g "' + nom_vid +
                  '.rar" "' + nom_vid + '.mp4"')
    else:
        print('winrar.exe a -afrar -df -m5 -mt3 -ri15 -t -tk -ts -v14g "' + nom_vid +
              '.rar" "' + nom_vid + '.mp4"')
        os.system('winrar.exe a -afrar -df -m5 -mt3 -ri15 -t -tk -ts -v14g "' + nom_vid +
                  '.rar" "' + nom_vid + '.mp4"')

main("1115073477")
main("1116064234")
main("1117082573")
#main("1117086452")
