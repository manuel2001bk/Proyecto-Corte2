import asyncio
import threading
import requests

def get_response(response):
    res = response.get('results')
    print(res, '\n')


def get_error():
    print("Respuesta erronea")


def insert_txt(gender, name, location):
    f = open('Proyecto-Corte2/salida_info.txt', 'w')
    f.write(gender)
    f.write(name)
    f.write(location)
    f.close


def insert_Db(gender, name, location):
    pass


async def solicitud(url, success_callback, error_callback):
    print('Inicia metodo')
    resultado = await metodo(url, success_callback, error_callback)

    gender = resultado.get('results')[0].get('gender')
    name = resultado.get('results')[0].get('name')
    location = resultado.get('results')[0].get('location')

    threading.Thread(target=insert_txt, kwargs={
        "gender": gender,
        "name": name,
        "location": location
    }).start()

    threading.Thread(target=insert_Db, kwargs={
        "gender": gender,
        "name": name,
        "location": location
    }).start()

    return True


async def metodo(url, success_callback, error_callback):
    res = requests.get(url)
    if res.status_code == 200:
        success_callback(res.json())
    else:
        error_callback()
    return res.json()


async def servicio(url, success_callback, error_callback):
    event = asyncio.get_event_loop()
    try:
        value = event.run_until_complete(
            solicitud(url, success_callback, error_callback))
        print('El retorno es ', value)

    finally:
        event.close()

if __name__ == '__main__':
    threading.Thread(target=servicio, kwargs={
        "url": "https://randomuser.me/api/",
        "success_callback": get_response, 
        "error_callback": get_error,
    }).start()
