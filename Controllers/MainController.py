
from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
from Models.Vrijeme import Vrijeme
from Models.TrenutnoVrijeme import TrenutnoVrijeme
from Models.Kontakt import Kontakt

from datetime import datetime, timedelta
import datetime

def setup(app: Flask, sesija):  # Controller sada oblikujemo kao factory funkciju koja radi rute i ono što se na njima događa

    def vratiDanUTjednu(timestamp,datum):
        daniUtjednu = ["Ponedjeljak","Utorak","Srijeda","Četvrtak","Petak","Subota","Nedjelja"]
        timestampObjekt = datetime.datetime.utcfromtimestamp(timestamp)
        print(f"timestampObjekt: {timestampObjekt}")
        redniBrojDana=timestampObjekt.weekday()
        return daniUtjednu[redniBrojDana]
    
    
    @app.route('/pokaziPrognozu')
    def pokaziPrognozu():
        return render_template("pokaziPrognozu.html", data=None, data2=None, data3=None)
    
    @app.route('/pocetnaStranica')
    def pocetnaStranica():
        return render_template('pocetnaStranica.html', porukaTekst="")

    @app.route('/kontakt')

    def kontakt():
        sviKontakti = sesija.query(Kontakt).all()
        return render_template('kontakt.html', data=sviKontakti)


    @app.route('/jednodnevna', methods=['POST', "GET"])
    def jednodnevna():
        if request.method == "GET":
            return render_template('jednodnevna.html', temperatura="")
        else:
            lokacija = request.form.get('lokacija')
            API_KEY = "ea21a50a658835f4b568483f65e25cbd"
            base_url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {'q': lokacija, 'appid': API_KEY, 'units': 'metric','lang':'hr'}

            try:
                response = requests.get(base_url, params=params, headers={
                    'Content-Type': 'application/json; charset=utf-8'})
            
                #response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    vrijemeDohvacanja = datetime.datetime.now()
                    datum=vrijemeDohvacanja
                    timestamp=data['dt']
                    
                    timestampSljedecegDohvacanja=timestamp+86400
                    temperatura = data['main']["temp"]
                    temperatura = f"{temperatura:.2f}"
                    osjecajTemperatura = data['main']["feels_like"]
                    osjecajTemperatura = f"{osjecajTemperatura:.2f}"
                    maksimalnaDnevna=data['main']["temp_max"]
                    maksimalnaDnevna = f"{maksimalnaDnevna:.2f}"
                    minimalnaDnevna = data['main']["temp_min"]
                    minimalnaDnevna = f"{minimalnaDnevna:.2f}"
                    vlaznost=data['main']['humidity']
                    brzinaVjetra = data['wind']['speed']
                    tlak= data['main']['pressure']

                    vrijemeSljedecegDohvacanja= vrijemeDohvacanja + timedelta(hours=2)
                    vrijeme = TrenutnoVrijeme(Datum = datum, Grad=lokacija, Temperatura = temperatura, OsjecajTemperatura = osjecajTemperatura, MaksimalnaDnevna=maksimalnaDnevna, MinimalnaDnevna=minimalnaDnevna, BrzinaVjetra= brzinaVjetra, Tlak=tlak, Vlaznost=vlaznost, VrijemeDohvacanja = vrijemeDohvacanja, VrijemeSljedecegDohvacanja= vrijemeSljedecegDohvacanja, Timestamp=timestamp, TimestampSljedecegDohvacanja=timestampSljedecegDohvacanja)

                    sesija.add(vrijeme)
                    sesija.commit()
                    return render_template("pokaziPrognozu.html", data=vrijeme, data2=None, data3=None)
                else:
                    return None
            except Exception as e:
                sesija.rollback()
                print(f'Greška pri dohvaćanju prognoze vremena: {e}')
                return render_template("jednodnevna.html", porukaTekst=f"Greška pri dohvaćanju prognoze vremena: {e}")


    @app.route('/visednevna', methods=['POST', "GET"])
    def visednevna():
        if request.method == "GET":
            return render_template('visednevna.html')
        else:
            lokacija = request.form.get("lokacija")
            cnt = str(int(3*24/3))
            API_KEY = 'ea21a50a658835f4b568483f65e25cbd'

            # /data/2.5/forecast' korisiti se za dohvacanje vise dana
            base_url = 'https://api.openweathermap.org/data/2.5/forecast'

            params = {'q': lokacija, 'appid': API_KEY, 'units': 'metric', 'cnt': cnt,'lang':'hr'}
            
            try:
                response = requests.get(base_url, params=params, headers={
                    'Content-Type': 'application/json; charset=utf-8'})
                data = response.json()

                if response.status_code == 200:
                    prognoza = []
                    prognoza2=[]
                    prognozaObjekti={} # datum : {datum, grad, temperatura itd}
                    for index, dan in enumerate(data['list']):
                        timestamp=dan['dt']
                        timestampSljedecegDohvacanja=timestamp+86400
                        #print(f"Timestamp: {timestamp}")
                        datum=dan['dt_txt']
                        danUTjednu=vratiDanUTjednu(timestamp,datum)
                        vrijemeDohvacanja = datetime.datetime.now()
                        vrijemeSljedecegDohvacanja= vrijemeDohvacanja + timedelta(hours=24)
                        temperatura = dan['main']['temp']
                        osjecajTemperatura = dan['main']['feels_like']
                        maksimalnaDnevna=dan['main']['temp_max']
                        minimalnaDnevna = dan['main']['temp_min']
                        tlak= dan['main']['pressure']
                        uvjeti = dan['weather'][0]['description']
                        icon=dan['weather'][0]['icon']
                        ikona=f"https://openweathermap.org/img/wn/{icon}@2x.png"
                        
                        vlaznost=dan['main']['humidity']
                        vjetar = dan['wind']
                        brzinaVjetra=vjetar['speed']
                        
                        '''vrijeme = Vrijeme(Datum = datum, Temperatura = temperatura, OsjecajTemperatura = osjecajTemperatura, MaksimalnaDnevna=maksimalnaDnevna, BrzinaVjetra= brzinaVjetra, DanUTjednu=danUTjednu, Tlak=tlak, Icon=icon, ikona=ikona,Uvjeti = uvjeti, Vlaznost=vlaznost, Vjetar =vjetar, VrijemeDohvacanja = vrijemeDohvacanja, VrijemeSljedecegDohvacanja= vrijemeSljedecegDohvacanja, Timestamp=timestamp, TimestampSljedecegDohvacanja=timestampSljedecegDohvacanja)'''

                        vrijeme = Vrijeme(Datum = datum, Grad=lokacija, Temperatura = temperatura, OsjecajTemperatura = osjecajTemperatura, MaksimalnaDnevna=maksimalnaDnevna, MinimalnaDnevna=minimalnaDnevna, BrzinaVjetra= brzinaVjetra, DanUTjednu=danUTjednu, Tlak=tlak, Vlaznost=vlaznost, VrijemeDohvacanja = vrijemeDohvacanja, VrijemeSljedecegDohvacanja= vrijemeSljedecegDohvacanja, Timestamp=timestamp, TimestampSljedecegDohvacanja=timestampSljedecegDohvacanja, Ikona=ikona)
                        
                        prognoza.append(
                            {"redniBroj": index, "temperatura": temperatura, "uvjeti": uvjeti,"redniBroj": index, "temperatura": temperatura, "uvjeti": uvjeti,"redniBroj": index, "temperatura": temperatura, "uvjeti": uvjeti})
                        
                        prognozaObjekti[datum]=vrijeme
                        prognoza2.append(vrijeme)
                        postojiLiVec = sesija.query(Vrijeme).get(datum)
                        if postojiLiVec is None:
                            sesija.add(vrijeme)
                            sesija.commit()
                        else:
                            sesija.rollback()
                        for objektVrijeme in prognozaObjekti:
                            print(f"Objekt s vremenom {datum}: {objektVrijeme}")
                        
                    #return render_template("pokaziPrognozu.html", data=prognoza, data2=prognoza2, data3=prognozaObjekti)
                    return render_template("pokaziPrognozu.html", data=prognoza2, data2=prognoza, data3=prognozaObjekti), 200, {'Location': '/pokaziPrognozu'}

                
                else:
                    return None
            except Exception as e:
                sesija.rollback()
                print(f'Greška pri dohvaćanju prognoze vremena: {e}')
                return render_template("visednevna.html", porukaTekst=f"Greška pri dohvaćanju prognoze vremena: {e}")

    app.add_url_rule("/", "pocetnaStranica", pocetnaStranica)



    # @app.route("/five_days")
    # def five_days():
      #  return render_template("pokaziPrognozu.html")


    
    '''   
    @app.route('/api/vrijeme', methods=['GET'])
    def apiVrijeme():
        grad = request.args.get('grad')
        if not grad:
            return jsonify({"error": "Niste naveli grad."}), 400''' 

    app.add_url_rule("/", "index", pocetnaStranica)

'''
prognoza = dohvati_prognozu_vremena(grad, cnt=5)

if prognoza:
    # u ovom slucaju ne koristi se json jer ti treba lista po kojoj mozes iterirati na html-u
    return render_template('index.html', data=prognoza)
else:
    return jsonify({"error": "Nije moguće dohvatiti prognozu vremena."})'''


'''
def dohvati_prognozu_vremena(grad, cnt):
    API_KEY = 'ea21a50a658835f4b568483f65e25cbd'

    # /data/2.5/forecast' korisiti se za dohvacanje vise dana
    base_url = 'https://api.openweathermap.org/data/2.5/forecast'

params = {'q': grad, 'appid': API_KEY, 'units': 'metric', 'cnt': cnt}

try:
    response = requests.get(base_url, params=params, headers={
        'Content-Type': 'application/json; charset=utf-8'})
    data = response.json()

    if response.status_code == 200:
        prognoza = []
        for dan in data['list']:
            temperatura = dan['main']['temp']
            uvjeti = dan['weather'][0]['description']
            prognoza.append({"temperatura": temperatura, "uvjeti": uvjeti})

        return prognoza
    else:
        return None
except Exception as e:
    print(f'Greška pri dohvaćanju prognoze vremena: {e}')
    return None'''