import sqlite3
import requests
from datetime import datetime

def sqlconnection():
    connection = sqlite3.connect('saatiedot.db')
    return connection

def create_table():
    connection = sqlconnection()   #kutsutaan sqlconnection funktiota joka palauttaa connection muuttujan tiedot
    cursor = connection.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS paikkakunnat (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nimi TEXT NOT NULL )
                ''')
    connection.commit()
    connection.close()

def checkpaikkakunnat(paikkakunnat):
    connection = sqlconnection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM paikkakunnat')
    for paikkakunta in paikkakunnat:
        cursor.execute('INSERT INTO paikkakunnat (nimi) VALUES (?)' , (paikkakunta,))
    connection.commit()
    connection.close()


def hae_paikkakunnat():
        connection = sqlconnection()
        cursor = connection.cursor()
        cursor.execute('SELECT nimi FROM paikkakunnat')
        paikkakunnat = [row[0] for row in cursor.fetchall()]
        connection.close()
        return paikkakunnat

#haetaan tiedot ilmatieteen laitoksen sivuilta
def hae_lampotila(paikkakunta):
    try:
        apikey = '5c6b02024c7f431d58eb7c7fc17cf0b6'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={paikkakunta}&appid={apikey}&units=metric'
        response = requests.get(url)
      
        if response.status_code == 200:
            data = response.json()
            
            if 'main' in data and 'temp' in data['main'] and 'feels_like' in data['main']:
                print(f"Lämpötila {paikkakunta}: {data['main']['temp']} °C")
                print(f"Koettu lämpötila {paikkakunta}: {data['main']['feels_like']} °C")
                return data['main']['feels_like']
            else:
                print(f"Lämpötilatiedot eivät löytyneet paikkakunnalta {paikkakunta}.")
                return None
        else:
            print(f"Virhe API-pyynnössä: {response.status_code}")
            return None

    except Exception as e:
        print(f"Virhe haettaessa lämpötilaa: {str(e)}")
        return None


