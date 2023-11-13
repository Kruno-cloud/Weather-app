from sqlalchemy import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__, static_folder="Assets", template_folder="Views")


engine = create_engine("sqlite:///Assets/Baza.db",
                       connect_args={"check_same_thread": False})
DBSession = sessionmaker(bind=engine)
sesija = DBSession()


def dohvati_prognozu_vremena(grad, cnt):
    API_KEY = 'ea21a50a658835f4b568483f65e25cbd'

    # /data/2.5/forecast' korisiti se za dohvacanje vise dana
    base_url = 'https://api.openweathermap.org/data/2.5/forecast'

    params = {'q': grad, 'appid': API_KEY, 'units': 'metric', 'cnt': cnt}

    try:
        response = requests.get(base_url, params=params)
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
        return None


@app.route('/')
def pocetna_stranica():
    return render_template('index.html')


@app.route('/api/vrijeme', methods=['GET'])
def api_vrijeme():
    grad = request.args.get('grad')
    if not grad:
        return jsonify({"error": "Niste naveli grad."}), 400

    prognoza = dohvati_prognozu_vremena(grad, cnt=5)

    if prognoza:
        # u ovom slucaju ne koristi se json jer ti treba lista po kojoj mozes iterirati na html-u
        return render_template('index.html', data=prognoza)
    else:
        return jsonify({"error": "Nije moguće dohvatiti prognozu vremena."})


@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')


if __name__ == '__main__':
    app.run(debug=True)
