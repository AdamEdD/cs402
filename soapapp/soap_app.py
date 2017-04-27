"""
Soap service to get Country info based on user input
"""
import zeep

from flask import Flask, render_template, request
app = Flask(__name__)

def countryinfo(Country):
    """
    function to read and return country data from wsdl on user input
    
    wsdl = http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL
    """
    wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
    client = zeep.Client(wsdl=wsdl)
    iso = client.service.CountryISOCode(Country)  
    conversion = currency(Country)
    CapCity = client.service.CapitalCity(iso)
    loc = location(CapCity)
    Cur = client.service.CountryCurrency(iso)
    flag = client.service.CountryFlag(iso)
    return [[Country,CapCity,loc[0],loc[1],Cur["sName"],conversion],flag]

from geopy.geocoders import Nominatim

def location(Capital):
    """
    Calculate lat and lon from wsdl Capital data
    return lat,lon
    """
    geolocator = Nominatim()
    location = geolocator.geocode(Capital)
    loc = [location.latitude, location.longitude]
    return loc

from currency_converter import CurrencyConverter
import money

def currency(Country):
    """
    Calculate and return currency conversion rate from euro
    """
    country_name = Country
    
    for currency, data in money.CURRENCY.iteritems():
        if country_name.upper() in data.countries:
            cur = currency
            c = CurrencyConverter()
            try:
                conversion = c.convert(1, 'EUR', cur)
            except KeyError:
                conversion = "Sorry no conversion information"
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
        try:
            result = countryinfo(v)
        except AttributeError or UndefinedError:
            result = [["Null","Null",0,0,"Null","Null"],0]
            break
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)