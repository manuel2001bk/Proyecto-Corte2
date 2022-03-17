import asyncio
import json
import threading
import requests
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="programacion_Acti",
    password="kPLeZo%N4xbN8y&Z!x1x",
    database="concurrente"
)

mycursor = mydb.cursor()


async def insertar_gender(genter):
    sql = "INSERT INTO gender (idgender,gender) VALUES (%s,%s)"
    val = ('0', genter)
    mycursor.execute(sql, val)
    mydb.commit()
    if (mycursor.rowcount > 0):
        print('Gender guardado con exito')


async def insertar_name(name):
    sql = "INSERT INTO name (title, first, last) VALUES (%s, %s ,%s)"
    val = (name.get('title'), name.get('first'), name.get('last'))
    mycursor.execute(sql, val)
    mydb.commit()
    if (mycursor.rowcount > 0):
        print('Name guardado con exito')


async def insertar_location(location):
    sql = "INSERT INTO location (street_number,street_name,city,state,country,postcode,coordinates_latitud,coordinates_longitud,timezone_offset,timezone_description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (location.get('street').get('number'), location.get('street').get('name'), location.get('city'), location.get('state'), location.get('country'),
           location.get('postcode'), location.get('coordinates').get('latitude'), location.get('coordinates').get('longitude'), location.get('timezone').get('offset'), location.get('timezone').get('description'))
    mycursor.execute(sql, val)
    mydb.commit()
    if (mycursor.rowcount > 0):
        print('location guardado con exito')


async def insert_txt(gender, name, location):
    f = open('salida_info.txt', 'a')
    f.write("\ngenter: ")
    f.write(gender)
    f.write("\nname: ")
    f.write(json.dumps(name))
    f.write("\nlocation: ")
    f.write(json.dumps(location))
    f.close
    print('Datos guardados en txt correctamente')


async def insert_Db(gender, name, location):

    await insertar_gender(gender)
    await insertar_name(name)
    await insertar_location(location)


async def solicitud(url):
    print('Inicia metodo de solicitudes')
    for i in range(200):
        print('Iniciando solicitud: ', i+1)
        resultado = await metodo(url)

        gender = resultado.get('results')[0].get('gender')
        name = resultado.get('results')[0].get('name')
        location = resultado.get('results')[0].get('location')
        await insert_txt(gender, name, location)
        await insert_Db(gender, name, location)
        print('Solicitud ', i+1, 'finalizada')


async def metodo(url):
    res = requests.get(url)
    if res.status_code == 200:
        print("Solicitud correcta")
    else:
        print("Solicitud incorrecta")
    return res.json()


def servicio(url):
    event = asyncio.new_event_loop()
    asyncio.set_event_loop(event)
    try:
        event.run_until_complete(solicitud(url))

    finally:

        event.close()


if __name__ == '__main__':
    threading.Thread(target=servicio, kwargs={
        "url": "https://randomuser.me/api/",
    }).start()
