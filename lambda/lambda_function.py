"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
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
    return alexa.create_response(message="Hello Welcome to My Recipes!")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent_handler("NextTrainIntent")
def next_train_intent_handler(request):
    """
    You can insert arbitrary business logic code here    
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    station = request.slots["Station"] 
    if station == None:
        return alexa.create_response("Please specify a station name.")

    card = alexa.create_card(title="NextTrainIntent activated", subtitle=None,
                             content="asked Alexa for next train to {}".format(station))

    return alexa.create_response("Looking up next train(s) to {}".format(station),
                                 end_session=False, card_obj=card)

