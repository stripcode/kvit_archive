from flask import Flask, Response
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from datetime import datetime
import re



def handler1(number, date):
  if re.match("^0037[0-9]{1,}$", number):
    wsdl = 'http://example.ru:180/uk2/ws/QueryKvit?wsdl'
    inn = '6625040375'
  elif re.match("^038[0-9]{1,}$", number):
    wsdl = 'http://example.ru:180/uk3/ws/QueryKvit?wsdl'
    inn = '6625052243'
  elif re.match("^[0-2][0-9]{1,3}$", number):
    wsdl = 'http://example.ru:180/QueryKvit/ws/QueryKvit?wsdl'
    inn = '6625052243'
  elif re.match("^[5-9][0-9]{1,3}$", number):
    wsdl = 'http://example.ru:180/uk1/ws/QueryKvit?wsdl'
    inn = '6625043023'
  elif re.match("^.{11}$", number): #alfa
    wsdl = 'http://example.ru:180/uk4/ws/QueryKvit?wsdl'
    inn = '6625061505'
  else:
    return "Не смогла распознать организацию", 400

  session = Session()
  session.auth = HTTPBasicAuth("hl_site", "Gs20yer")
  client = Client(wsdl = wsdl, transport = Transport(session = session, timeout = 10))

  day = datetime.strptime(date, "%Y-%m-%d")
  res = client.service.Qvery(inn, day, number)
  response = Response(res)
  response.headers["Content-Type"] = "application/pdf"
  return response



KEYS = {
  "14c59283f1589b571ac6c1fbb857bbdc044ae83c": handler1
}


app = Flask(__name__)


@app.route("/api/<key>/<number>/<date>")
def getKvit(key, number, date):
  if key in KEYS:
    func = KEYS[key]
    return func(number, date)
  else:
    return "Нет такого ключа", 404



if __name__ == "__main__":
  app.run(debug = True, host = "0.0.0.0")