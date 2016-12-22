"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
from bart_trip import BartTrip
from station_codes import station_code
import datetime
from time import strftime

API_KEY = 'MW9S-E7SL-26DU-VV8V'
ORIGIN = 'GLEN'

def lambda_handler(request_obj, context=None):
    '''
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {}
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="PogoBart launched")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="PogoBart signoff")


@alexa.intent_handler("NextTrainIntent")
def next_train_intent_handler(request):
    # Get variables like userId, slots, intent name etc from the 'Request' object
    station = request.slots["Station"] 
    if station == None:
        return alexa.create_response("Please try again, giving the destination station name.")
    result = get_trips(station, 'depart')
    return deliver_result(station,result)

@alexa.intent_handler("ArriveTimeIntent")
def arrive_intent_handler(request):
    station = request.slots["Destination"]
    arrive_time = request.slots["Time"]
    if (station == None or arrive_time == None):
        return alexa.create_response("Please try again, giving the destination station and arrival time.")
    result = get_trips(station, 'arrive', arrive_time)
    return deliver_result(station,result)


@alexa.intent_handler("DelaysIntent")
def delays_intent_handler(request):
    delays = BartTrip(API_KEY)
    result = "DelaysIntent activated"
    if delays.error:
        speak = "Sorry. {}".format(delays.error)
        result = "DelaysIntent error"
    elif delays.delays:
        speak = delays.delays
    else:
        speak = "No delays reported."
    card = alexa.create_card(title = result, subtitle=None, content=speak)
    return alexa.create_response(speak,end_session=True,card_obj=card)
    
def deliver_result(station,result):
    if result.error:
        card = alexa.create_card(title = "NextTrainIntent error", subtitle=None,
                                 content = result.error)
        return alexa.create_response("Sorry. {}".format(result.error), end_session=True, card_obj=card)
    else:
        card = alexa.create_card(title="NextTrainIntent activated", subtitle=None,
                                 content="asked Alexa for trains to {}".format(station))
        speak = format_trips(station, result)
        return alexa.create_response(speak, end_session=True, card_obj=card)

def format_trips(station,result):
    trips = result.trips
    if result.cmd == 'arrive':
        s = "To arrive at {} by {}, you can depart at ".format(station, strftime('%-I %M %p', result.time))
    else:
        s = "The next {} trains to {} depart at ".format(len(trips),station)
    trips[-1] = "and {}".format(trips[-1])
    s += ", ".join(trips)
    # delays?
    if result.delays:
        s += ". But " + result.delays + "."
    else:
        s += ", with no delays reported."
    return s

'''
def format_trips(station,trips):
    s = "The next {} trains to {} depart in ".format(len(trips),station)
    times = map(minutes_from_now, trips)
    times_spoken = map(lambda t: "{} minutes".format(t), times)
    times_spoken[-1] = "and {}".format(times_spoken[-1])
    s += ", ".join(times_spoken)
    return s
'''
def minutes_from_now(time_as_str):
    now = datetime.datetime.now()
    now = now.replace(year=1900,month=1,day=1)
    time = datetime.datetime.strptime(time_as_str, '%I:%M %p')
    # if time given is between midnight and 3 am, but current time
    # is EARLIER than midnight, make 'now' be the next day so time
    # arithmetic works out
    if (time.hour <= 3 and now.hour <= 3):
        now = now.replace(day=2)
    return ((time - now).seconds) / 60

def get_trips(station,cmd,time=None):
    bart = BartTrip(API_KEY)
    dest = station_code(station)
    if dest == None:
        bart.error = "I don't recognize the station name {}".format(station)
    else:
        bart.get_trips(ORIGIN, dest, cmd, time)
    return bart


