import zeep
#wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
def countryinfo():
    Country = raw_input("Enter a Country: ")
    wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
    client = zeep.Client(wsdl=wsdl)
    iso = client.service.CountryISOCode(Country)

    CapCity = client.service.CapitalCity(iso)
    Cur = client.service.CountryCurrency(iso)
    flag = client.service.CountryFlag(iso)
    print("\nCountry: %s \nCapital: %s \nCurrency: %s \nflag: %s \n"%(Country,CapCity,Cur["sName"],flag))
    
countryinfo()