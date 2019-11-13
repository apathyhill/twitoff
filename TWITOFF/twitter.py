import basilica
from twython import Twython
from decouple import config

twitter_client = Twython(config("API_KEY"),
						 config("API_SECRET"), 
						 config("CONSUMER_KEY"),
						 config("CONSUMER_SECRET"))

basilica_client = basilica.Connection(config("BASILICA_KEY"))

