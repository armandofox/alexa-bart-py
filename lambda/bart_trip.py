import urllib
import urllib2
import re
from xml.dom import minidom

class BartTrip(object):

    DEFAULT_KEY = 'MW9S-E7SL-26DU-VV8V'
    ENDPOINT = 'http://api.bart.gov/api/'

    def __init__(self, key=DEFAULT_KEY):
        self.key = key
        self.body = ''
        self.error = None
        self.trips = None
        self.delays = None

    def get_trips(self,orig,dest):
        body = self.retrieve_schedule(orig,dest)
        '''
        Schema: j.root.schedule.request.trip is an array of trip objects
            Within a trip object t, t.attr['origTimeMin'] looks like "6:14 PM", t.leg is array of legs
            (first leg in the XML usually seems to be first trip leg, but there s also a l.order elt)
           Within a leg l, l.trainHeadStation is station code where that train is headed, eg PITT
        '''
        self.parse_response()
        self.get_delays()

    def parse_response(self):
        dom = minidom.parseString(self.body)
        trips = dom.getElementsByTagName('trip')
        self.trips = map(lambda trip: trip.getAttribute('origTimeMin'), trips)

    def retrieve_schedule(self,orig,dest):
        params = {
            'cmd': 'depart',
            'b': '0',
            'a': '3',
            'orig': orig,
            'dest': dest,
            'key': self.key
        }
        url = '{}/sched.aspx?{}'.format(self.ENDPOINT, urllib.urlencode(params))
        try:
            self.body = urllib2.urlopen(url).read()
        except urllib2.URLError:
            self.error = 'The BART website did not respond'

    def get_delays(self):
        params = { 'key': self.key, 'cmd': 'bsa', 'date': 'today' }
        url = '{}/bsa.aspx?{}'.format(self.ENDPOINT, urllib.urlencode(params))
        try:
            body = urllib2.urlopen(url).read()
            delay_elts = minidom.parseString(body).getElementsByTagName('description')
            delays = map(lambda elt: elt.firstChild.wholeText, delay_elts)
            l = len(delays)
            if l == 0 or (l == 1 and re.match(r'No delays reported',delays[0])):
                pass
            else:
                self.delays = ". And ".join(delays)
        except urllib2.URLError:
            self.error = "I couldn't get delay information."
