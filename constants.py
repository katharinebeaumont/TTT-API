
from os import environ
from rdflib import URIRef

### Constants ###

#Game Ontology
GAME_ONTOLOGY="TicTacToe.owl"
GAME_ONTOLOGY_TAG="tic-tac-toe"
GAME_ONTOLOGY_PREFIX="ttt"

#Server stuff
HOST=environ.get('HOST', 'localhost')
PORT=environ.get('PORT', 8083)

BASE_URL='http://'+HOST+':'+str(PORT)+'/'

#Internal Game Bot
BOT_NAME = "apibot"
API_BOT_URI = URIRef(BASE_URL + BOT_NAME)