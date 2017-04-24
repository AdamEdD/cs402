import zeep

from flask import Flask, render_template, request
app = Flask(__name__)

def countryinfo(Country):
    #Country = raw_input("Enter a Country: ")
    wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
    client = zeep.Client(wsdl=wsdl)
    iso = client.service.CountryISOCode(Country)
    conversion = currency(Country)
    CapCity = client.service.CapitalCity(iso)
    loc = location(CapCity)
    Cur = client.service.CountryCurrency(iso)
    flag = client.service.CountryFlag(iso)
    return [[Country,CapCity,Cur["sName"],conversion],flag,loc]

from geopy.geocoders import Nominatim

def location(Capital):
    geolocator = Nominatim()
    location = geolocator.geocode(Capital)
    loc = [location.latitude, location.longitude]
    return loc

from currency_converter import CurrencyConverter
import money

def currency(Country):
    country_name = Country
    
    for currency, data in money.CURRENCY.iteritems():
        if country_name.upper() in data.countries:
            cur = currency
            c = CurrencyConverter()
            conversion = c.convert(1, 'EUR', cur)
            return conversion
            break

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      for k,v in result.iteritems():
        result = countryinfo(v)    
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)