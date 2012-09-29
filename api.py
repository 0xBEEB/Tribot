from time import localtime, time
from urllib2 import urlopen
from xml.dom.minidom import parseString
import json

from settings import APP_ID

BASE_URI = 'http://developer.trimet.org/ws/V1/'
GOOG_URI = 'http://maps.googleapis.com/maps/api/geocode/json?'


def getArrivals(stopID):
    """
    getArrivals

    Returns the estimated arrival times of the buses for a given stop ID

    :param:     stopID  Long
    :return:    time    time_t
    """
    url = "%sarrivals?appID=%s&locIDs=%s" % (BASE_URI, APP_ID, stopID)
    f = urlopen(url)
    response = f.read()

    dom = parseString(response)
    arrivalElems = dom.getElementsByTagName("arrival")

    arrivals = []
    for arrival in arrivalElems:
        sign = arrival.getAttribute("fullSign")
        estimated = arrival.getAttribute("estimated")[:-3]
        if estimated == "":
            estimated = arrival.getAttribute("scheduled")[:-3]
        mins = (long(estimated) - int(time())) / 60
        arrivals.append("%s arriving in %s minutes" % (sign, mins))

    return arrivals


def getLatLong(address):
    """
    getLatLong

    Returns a dictionary of the lat long corresponding to the given address

    :param:     address str
    :return:    latlong dict
    """
    if "portland" not in address.lower():
        address += " Portland Oregon"
    url = "%saddress=%s&sensor=false" % (GOOG_URI, "+".join(address.split()))
    f = urlopen(url)
    response = f.read()

    data = json.loads(response)
    return data['results'][0]['geometry']['location']

def getStops(ll):
    """
    getStops

    Returns a list of stops based off of a lat long pair

    :param:     ll      { lat : float, lng : float }
    :return:    list
    """
    url = "%sstops?appID=%s&ll=%s,%s" % (BASE_URI, APP_ID, ll['lat'], ll['lng'])
    f = urlopen(url)
    response = f.read()

    dom = parseString(response)
    stopElems = dom.getElementsByTagName("location")

    stops = []
    for se in stopElems:
        locid = se.getAttribute("locid")
        desc = se.getAttribute("desc")
        direction = se.getAttribute("dir")
        stops.append("ID: %s, %s on %s" % (locid, direction, desc))

    return stops

def stopsByAddr(address):
    """
    stopsByAddr

    Returns stops near a text address

    :param:     address str
    :return:    list
    """
    return getStops(getLatLong(address))

def getAddress(ll):
    """
    getAddress

    Returns an address estimated from lat long pair

    :param:     ll      { lat, lng }
    :return:    str
    """
    url = "%slatlng=%s,%s&sensor=false" % (GOOG_URI, ll['lat'], ll['lng'])
    f = urlopen(url)
    response = f.read()

    data = json.loads(response)
    return data['results'][0]['formatted_address']

def busLastSeen(stopID, route):
    """
    busLastSeen

    Given a stopID and a route returns the last seen location of the bus

    :param:     stopID  int
    :param:     route   int
    :return:    str
    """
    url = "%sarrivals?appID=%s&locIDs=%s" % (BASE_URI, APP_ID, stopID)
    f = urlopen(url)
    response = f.read()

    dom = parseString(response)
    arrivalElems = dom.getElementsByTagName("arrival")

    for arrival in arrivalElems:
        arrivalRoute = arrival.getAttribute("route")
        if arrivalRoute == str(route):
            pos = arrival.getElementsByTagName("blockPosition")[0]
            seenAt = pos.getAttribute("at")[:-3]
            mins = (int(time()) - long(seenAt)) / 60
            location = getAddress(
                {
                    'lat' : pos.getAttribute("lat"),
                    'lng' : pos.getAttribute("lng")
                }
            )
            return "Your bus was last seen on %s %s minutes ago" % (location, mins)

    return "I'm sorry I don't have that information"

