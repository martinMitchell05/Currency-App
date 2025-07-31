from dotenv import load_dotenv
import os
import time
import requests
from datetime import datetime as dt

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")
URL = os.getenv("API_URL")
BLUE_URL = os.getenv("BLUE_URL")
HISTORICAL_BLUE = os.getenv("HISTORICAL_BLUE")


class CurrencyApp:
    def __init__(self):
        self._url = URL
        self._key = ACCESS_KEY
        self._urlBlue = BLUE_URL
        self._historyBlue = HISTORICAL_BLUE

    def getURL(self):
        return self._url
    
    def getURLBlue(self):
        return self._urlBlue
    
    def getURLHistoryBlue(self):
        return self._historyBlue
    
    def getKey(self):
        return self._key
    
    def _safeRequest(self, url : str, params : dict = None, retries=3, delay=1):
        for _ in range(retries):
            try:
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 429:

                    print("⚠️ Too many requests. Waiting before retrying...")
                    time.sleep(delay)
                    continue

                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e:

                print(f"❌ Error during request: {e}")
                time.sleep(delay)

        print("All attempts failed.")
        return None
    
    def getCurrenciesCod(self):
        endpoint = {
            "access_key": self.getKey()
        }

        return self._safeRequest(self.getURL() + "list",params=endpoint)
           

    def searchCod(self, moneda : str):
        cod = ""

        cods = self.getCurrenciesCod()

        if cods:
            for k,v in cods["currencies"].items():
                if (v == moneda):
                    cod = k
                    break

        return cod

    def convert(self,moneda_base : str, moneda_destino : str, monto : float):
        
        endpoint = {
            "access_key": self.getKey(),
            "from": moneda_base,
            "to": moneda_destino,
            "amount": monto
        }

        return self._safeRequest(self.getURL() + "convert",params=endpoint)
    

    def convert_history(self, moneda_base : str, moneda_destino : str, monto : float, fecha : dt):

        endpoint = {
            "access_key": self.getKey(),
            "from": moneda_base,
            "to": moneda_destino,
            "amount": monto,
            "date": fecha.strftime("%Y-%m-%d")
        }

        return self._safeRequest(self.getURL() + "convert",params=endpoint)
    

    def getCurrencies(self,base : str,monedas : list[str]):

        endpoint = {
            "access_key": self.getKey(),
            "currencies": ",".join(monedas),
            "source": base
        }

        return self._safeRequest(self.getURL() + "live",params=endpoint)
    
    def getCurrenciesHistory(self,base : str, monedas : list[str], fecha : dt):

        endpoint = {
            "access_key": self.getKey(),
            "currencies": ",".join(monedas),
            "source": base,
            "date": fecha.strftime("%Y-%m-%d")
        }

        return self._safeRequest(self.getURL() + "historical",params=endpoint)
    
    def getDolarBlue(self):
        response = self._safeRequest(self.getURLBlue())
        return response["blue"] if response else {}
    
    def convertDolarBlueToARS(self,monto_usd : float):
        result = 0.0
        sell_price = self.getDolarBlue()["value_sell"]
        if sell_price:
            result = sell_price * monto_usd
        
        return result
    
    def convertARSToDolarBlue(self, monto_ars : float):
        result = 0.0
        buy_price = self.getDolarBlue()["value_buy"]
        if buy_price and buy_price != 0:
            result = monto_ars / buy_price
        
        return result

    def getBlueHistory(self, fecha : dt):
        endpoint = {
            "day": fecha.strftime("%Y-%m-%d")
        }
        return self._safeRequest(self.getURLHistoryBlue(),params=endpoint)
    
    def getEuroBlue(self):
        response = self._safeRequest(self.getURLBlue())

        return response["blue_euro"] if response else {}
    
    def convertEuroBlueToARS(self, monto_eur : float):
        result = 0.0
        sell_price = self.getEuroBlue()["value_sell"]
        if sell_price:
            result = sell_price * monto_eur
        
        return result
    
    def convertARSToEuroBlue(self, monto_ars : float):
        result = 0.0
        buy_price = self.getEuroBlue()["value_buy"]
        if buy_price and buy_price != 0:
            result = monto_ars / buy_price

        return result

#if __name__ == "__main__":
    #aplicacion = CurrencyApp()

    ### PRUEBAS DE REQUESTS ###
    
    #historico = aplicacion.convert_history("ARS","USD",10000,dt(2023,7,11))
    #print(f"Monto en USD = ${historico["result"]} a la fecha de {historico["date"]}")

    #listado_historico = aplicacion.getCurrenciesHistory("USD",["ARS","EUR","CAD"],dt(2022,7,11))
    #for k,v in listado_historico["quotes"].items():
    #    base = k[:3]
    #    destino = k[3:]
    #    print(f"1 {base} = {v:.2f} {destino} a la fecha de {listado_historico["date"]}")

    #resultados = aplicacion.convert("EUR","ARS",3679.88)
    #print(f"{resultados["result"]:.2f} ARS")

    #codigos = aplicacion.getCurrenciesCod()
    #for k,v in codigos["currencies"].items():
    #    print(f"{k} = {v}")

    #listado = aplicacion.getCurrencies("CAD",["ARS","USD"])
    #for k,v in listado["quotes"].items():
    #    base = k[:3] #extrae los primeros 3 caracteres de la key. (forma la moneda base)
    #    destino = k[3:] #extrae los ultimos caracteres desde el tercero, de la key del dict en 'quotes'. (forma la moneda destino)
    #    print(f"1 {base} = {v:.2f} {destino}")

    #codigo_moneda = aplicacion.searchCod("British ")
    #if (codigo_moneda != ""):
    #   print(f"Codigo para la moneda ingresada: {codigo_moneda}")
    #else:
    #   print("El codigo o la moneda ingresada no existe")

    #blue = aplicacion.getDolarBlue()
    #for k,v in blue.items():
    #   print(f"{k} = ${v} ARS")

    #print(aplicacion.convertARSToDolarBlue(10000))
    #print(aplicacion.convertDolarBlueToARS(100))

    #historico = aplicacion.getBlueHistory(dt(2022,7,11))
    #for k,v in historico["blue"].items():
    #   print(f"{k} = ${v} ARS")

    #euro = aplicacion.getEuroBlue()
    #for k,v in euro.items():
    #   print(f"{k} = ${v} ARS")

    #print(aplicacion.convertARSToEuroBlue(20000))
    #print(f"\n{aplicacion.convertEuroBlueToARS(100)}")
