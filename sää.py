import sqlite3
import requests
import time
from datetime import datetime

def sqlconnection():
    connection = sqlite3.connect('saatiedot.db')
    return connection

def create_table():
    connection = sqlconnection()   #kutsutaan sqlconnection funktiota 
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

#haetaan tiedot sääpalvelusta
def hae_lampotila(paikkakunta):
    try:
        apikey = '5c6b02024c7f431d58eb7c7fc17cf0b6'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={paikkakunta}&appid={apikey}&units=metric'
        response = requests.get(url)
      
        if response.status_code == 200:
            data = response.json()
            
            if 'main' in data and 'temp' in data['main'] and 'feels_like' in data['main']:
                print('*' * 40) 
                print(f'Paikkakunta: {paikkakunta.upper()}')
                print(f"Lämpötila: {data['main']['temp']} °C")
                print(f"Koettu lämpötila: {data['main']['feels_like']} °C")
                
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


def log(paikkakunta, status, lisatieto=None):
    with open('saatiedot.log', 'a' , encoding='utf-8') as loki:
        aika = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if status == 'onnistui':
            loki.write(f'{aika} - {paikkakunta}: Lämpötilahaku onnistui: {lisatieto} °C\n')
        elif status == 'virhe':
            loki.write(f'{aika} - {paikkakunta}: hakuvirhe\n')


def main():
    create_table()
    while True:
        print("Valitse toiminto")
        print("1. Muuta seurattavia paikkakuntia")
        print("2. Hae lämpötilatiedot")
        print("3. Lopeta ohjelma")
        valinta = input("Valinta: ").strip()

        if valinta == '1':
            paikkakunnat = []
            print("Anna paikkakunta kerrallaan. Lopeta antamalla X.")
            while True:
                paikkakunta = input("Paikkakunta: ").strip()
                if paikkakunta.upper() == 'X':
                    break
                paikkakunnat.append(paikkakunta)
            checkpaikkakunnat(paikkakunnat)
            print("Paikkakunnat tallennettu")

        elif valinta == '2':
            time.sleep(2)
            paikkakunnat = hae_paikkakunnat()
            if not paikkakunnat:
                print("Ei seurattavia paikkakuntia. Lisää paikkakunta ensin")
                continue
        
            onnistuneet = 0
            for paikkakunta in paikkakunnat:
                lampotila = hae_lampotila(paikkakunta)
                if lampotila is not None:
                    print(f'Kirjoitettu lokiin : {paikkakunta}\t{lampotila} °C')
                      
                    log(paikkakunta, 'onnistui', lampotila)    #def log kirjoitetaan loki tällä kutsulla
                    onnistuneet += 1
                else:
                    print(f'{paikkakunta}\tHakuvirhe')
                    log(paikkakunta, 'virhe')
            
            print(f'Onnistuneet haut: {onnistuneet}/{len(paikkakunnat)}')
            print('*' * 40)  
            log('Yhteenveto', 'onnistui', f'{onnistuneet}/{len(paikkakunnat)} onnistui')
        
        elif valinta == '3':
            print('Ohjelma lopetetaan, kiitos ohjelman käytöstä.')
            print('...')
            time.sleep(2)
            print(f'Näkemiin!')
            time.sleep(2)
            break

        else:
            print(f'Virheellinen valinta. Tarkista syöte')

if __name__ == '__main__':
    main()




