from flask import Flask
from flask import request
import requests
import datetime

app = Flask(__name__)

###############################
# Esta función recibe argumentos del tipo 'aaaa-mm-dd' en un string, por ejemplo, '2007-07-22' el 22 de julio de 2007. Regresa la fecha en formato epoch.


def _traduceFecha_(fecha, dias=0):
    fecha = fecha.split('-', 3)
    fecha = int(
        datetime.datetime(int(fecha[0]), int(fecha[1]), int(fecha[2]), 0,
                          0).timestamp())
    if dias > 0:
        fecha + (
            dias * 86400
        )  #Si se requiere un intervalo de dias después de la fecha dada
    return fecha


#############################
# Funcion default para invocar al endpoint raiz.


@app.route("/")
def index():

    simbolo = request.args.get("simbolo", "")
    fechaini = request.args.get("fechaini", "")

    return """<form action="/series" method="get">
                <input type="text" name="simbolo">
                <input type="text" name="fechaini">
                <input type="submit" value="Desplegar">
              </form>""" + simbolo + fechaini


#######################################
# Esta función hace una solicitud a yahoo finance usando un simbolo en el intervalo de tiempo [fechainicio, fechafin]. Estas fechas tienen el formato aaaa-mm-dd. Posteriormente crea un archivo csv en el que hace una


@app.route("/series")
def yahooFinanceInfo():
    simbolo = request.args.get("simbolo", "")
    fechaini = request.args.get("fechaini", "")
    fechafin = str(datetime.date.today())
    path = ''

    # Primero tengo que obtener el valor "crumb", ese valor se tiene que agregar al url del archivo que se quiere descargar, así que se harán dos solicitudes get usando requests. La primera para obtener el crumb y luego para descargar el archivo.

    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (simbolo, simbolo)
    response = requests.get(url)
    cookie = {'B': response.cookies['B']}

    # Obteniendo el crumb para hacer la solicitud del archivo. Lo busco como un atributo CrumbStore, el cual tiene un valor de diccionario dentro del cual busco la llave crumb, la cual tiene por valor el crumb que busco.

    lines = response.content.decode("utf-8")
    crumb = lines.split('CrumbStore', 2)[1].split('crumb', 2)[1].split('"',
                                                                       3)[2]
    del lines

    # Solicitando a yahoo finance el archivo
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (
        simbolo, _traduceFecha_(fechaini), _traduceFecha_(fechafin, 1), crumb)
    response = requests.get(url, cookies=cookie)

    data = response.content.decode("utf-8").replace(" ", "")

    return """<form action="/series" method="get">
                <input type="text" name="simbolo">
                <input type="text" name="fechaini">
                <input type="submit" value="Desplegar">
              </form>""" + data


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
