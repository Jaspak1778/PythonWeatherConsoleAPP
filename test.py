import requests

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

# funktion kutsu
hae_lampotila('helsinki')
