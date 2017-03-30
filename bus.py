"""Assignment 4 - cs402
Write a program that can fetch this realtime xml feed for your chosen bus stop id,
parses it and displays the bus times in a more readable tabular form..

example BE stopid: "131841" (Virginia -> Cavan)
example BAC stopid: "1234"
"""
import urllib2
import datetime
import re
import speech_recognition as sr
import xmltodict
import pyttsx
import pprint
def readxml(query):
    """readxml
    parse the xml for the input stopid
    use input query to return different speech patterns
    ie if "next: in query return the next bus time
    retrun xml in nicer format - speech
    """
    engine = pyttsx.init()
    stopid = re.sub(r'\D', "", query)
    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    now = datetime.datetime.strptime(now, '%d/%m/%Y %H:%M:%S')
    busxml = urllib2.urlopen("https://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid="
                             + str(stopid) + "&format=xml")
    data = busxml.read()
    busxml.close()
    data = xmltodict.parse(data)
    print(data)
    keys = ['arrivaldatetime', 'destination', 'origin', 'route', 'operator']
    info = []
    for value in data.itervalues():
        try:
            length = (len(value.get('results').get('result')))
            for key in value.get('results'):
                for i in keys:
                    info.append(
                        [value.get('results')[key][index].get(i) for index in range(length)])
        except AttributeError:
            engine.say("Sorry, I didnt quite catch that. Please try again?")
    info = list(map(list, zip(*info)))
    if len(info) is not 0:
        engine.say("I will get that information now.")
    if 'next' in query:
        for i in info:
            then = (datetime.datetime.strptime(i[0], '%d/%m/%Y %H:%M:%S'))
            delta = ((then - now).total_seconds() / 60.0)
            if i[1] in query:
                if i[2] is None:
                    engine.say('The next service to %s is due in %s minutes.'
                               %(i[1], int(delta)))
                    break
                else:
                    engine.say('The next service to %s is due in %s minutes from %s.'
                               %(i[1], int(delta), i[2]))
                    break
            else:
                then = (datetime.datetime.strptime(info[0][0], '%d/%m/%Y %H:%M:%S'))
                delta = ((then - now).total_seconds() / 60.0)
                if info[0][2] is None:
                    engine.say('The %s %s service to %s is due in %s minutes.'%
                               (info[0][3], info[0][4], info[0][1], int(delta)))
                    break
                else:
                    engine.say('The %s %s service to %s is due in %s minutes from %s.'%
                               (info[0][3], info[0][4], info[0][1], int(delta), info[0][2]))
                    break
    else:
        for i in info:
            then = (datetime.datetime.strptime(i[0], '%d/%m/%Y %H:%M:%S'))
            delta = ((then - now).total_seconds() / 60.0)
            if i[2] is None:
                engine.say('The %s %s service to %s is due in %s minutes.'
                           %(i[3], i[4], i[1], int(delta)))
            else:
                engine.say('The %s %s service to %s is due in %s minutes from %s.'
                           %(i[3], i[4], i[1], int(delta), i[2]))
    engine.runAndWait()

def listen():
    """listen
    listen for user input
    pass input to readxml as query
    """
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print "Listening.."
        audio = rec.listen(source)
    try:
        print "Query = " + rec.recognize_google(audio)
        readxml(rec.recognize_google(audio))
    except sr.UnknownValueError:
        print "Google Speech Recognition could not understand audio"
    except sr.RequestError as err:
        print "Could not request results from Google Speech Recognition service; {0}".format(err)

listen()
