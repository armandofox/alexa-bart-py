import urllib
import urllib2
import re
from xml.dom import minidom
from time import strftime,strptime

class BartTrip(object):

    DEFAULT_KEY = 'MW9S-E7SL-26DU-VV8V'
    ENDPOINT = 'http://api.bart.gov/api/'

    def __init__(self, key=DEFAULT_KEY):
        self.key = key
        self.body = ''
        self.error = None
        self.trips = None
        self.delays = None
        self.time = None

    def get_trips(self,orig,dest,cmd,time=None):
        self.cmd = cmd
        self.origin = orig
        self.destination = dest
        if time==None:
            self.time = None
        else:
            self.time = strptime(time, '%H:%M')
        body = self.retrieve_schedule()
        self.parse_response()
        self.get_delays()

    def parse_response(self):
        dom = minidom.parseString(self.body)
        trips = dom.getElementsByTagName('trip')
        self.trips = map(lambda trip: trip.getAttribute('origTimeMin'), trips)

    def retrieve_schedule(self):
        params = {
            'cmd': self.cmd,
            'b': ('2' if self.cmd == 'arrive' else '0'),
            'a': ('0' if self.cmd == 'arrive' else '3'),
            'orig': self.origin,
            'dest': self.destination,
            'key': self.key
        }

        if not self.time == None:
            params['time'] = strftime('%-I:%M%p', self.time)

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
