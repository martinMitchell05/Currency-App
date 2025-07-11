from dotenv import load_dotenv
import os
import requests
from datetime import datetime as dt

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")
URL = os.getenv("API_URL")


class app:
    def __init__(self):
        self._url = URL
        self._key = ACCESS_KEY

    def getURL(self):
        return self._url
    
    def getKey(self):
        return self._key
    
    def getCurrenciesCod(self):

        endpoint = {
            "access_key": self.getKey()
        }

        result = requests.get(self.getURL() + "list",params=endpoint)

        return result.json()

    def searchCod(self, moneda : str):
        cod = ""

        cods = self.getCurrenciesCod()

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

        result = requests.get(self.getURL() + "convert",params=endpoint)
        
        return result.json()
    

    def convert_history(self, moneda_base : str, moneda_destino : str, monto : float, fecha : dt):

        endpoint = {
            "access_key": self.getKey(),
            "from": moneda_base,
            "to": moneda_destino,
            "amount": monto,
            "date": fecha.strftime("%Y-%m-%d")
        }

        result = requests.get(self.getURL() + "convert",params=endpoint)
        return result.json()
    

    def getCurrencies(self,base : str,monedas : list[str]):

        endpoint = {
            "access_key": self.getKey(),
            "currencies": ",".join(monedas),
            "source": base
        }

        result = requests.get(self.getURL() + "live",params=endpoint)
        return result.json()
    
    def getCurrenciesHistory(self,base : str, monedas : list[str], fecha : dt):

        endpoint = {
            "access_key": self.getKey(),
            "currencies": ",".join(monedas),
            "source": base,
            "date": fecha.strftime("%Y-%m-%d")
        }

        result = requests.get(self.getURL() + "historical",params=endpoint)

        return result.json()


if __name__ == "__main__":
    aplicacion = app()

    ### PRUEBAS DE REQUESTS ###
        
    #resultados = aplicacion.convert("CAD","USD",80000)
    #print(f"80000 CAD = {resultados["result"]} USD")

    #listado = aplicacion.getCurrencies("EUR",["ARS","USD","AUD"])
    #for k,v in listado["quotes"].items():
     #   base = k[:3] #extrae los primeros 3 caracteres de la key. (forma la moneda base)
      #  destino = k[3:] #extrae los ultimos caracteres desde el tercero, de la key del dict en 'quotes'. (forma la moneda destino)
       # print(f"1 {base} = {v:.2f} {destino}")
    
    #historico = aplicacion.convert_history("ARS","USD",10000,dt(2023,7,11))
    #print(f"Monto en USD = ${historico["result"]} a la fecha de {historico["date"]}")

    #listado_historico = aplicacion.getCurrenciesHistory("USD",["ARS","EUR","CAD"],dt(2022,7,11))
    #for k,v in listado_historico["quotes"].items():
     #   base = k[:3]
      #  destino = k[3:]
       # print(f"1 {base} = {v:.2f} {destino} a la fecha de {listado_historico["date"]}")
    
    #codigos = aplicacion.getCurrenciesCod()
    #for k,v in codigos["currencies"].items():
     #   print(f"{k} = {v}")

    #codigo_moneda = aplicacion.searchCod("Canadian Dollar")
    #if (codigo_moneda != ""):
     #   print(f"Codigo para la moneda ingresada: {codigo_moneda}")
    #else:
     #   print("El codigo o la moneda ingresada no existe")