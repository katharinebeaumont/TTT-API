# Need: Define class and supported properties (e.g. 9 https://www.hydra-cg.com/spec/latest/core/#example-9-defining-a-class-and-documenting-its-supported-properties)
# Forms? IRITemplate - map things to paremters needed for endpoint
# Who is responsible for working out the winner? Is it for the agent or the opponent. or the board.
import requests
import pandas as pd
import numpy as np
import json
from flask import Flask,request,Response,redirect,render_template,send_file,current_app
from os import environ
from rdflib import Graph, URIRef, Namespace, RDF
from graphhelpermethods import GraphHelperMethods
from werkzeug.routing import BaseConverter
# HOSTING THE ONTOLOGY https://github.com/RDFLib/pyLODE
from pylode import OntDoc
import uuid
import io
import pydotplus
from IPython.display import display, Image
from rdflib.tools.rdf2dot import rdf2dot

from responsewriter import ResponseWriter
from apibot import APIBOT

# Constants
HOST=environ.get('HOST', 'localhost')
PORT=environ.get('PORT', 8083)
BASE_URL='http://'+HOST+':'+str(PORT)+'/'
API_BOT = URIRef(BASE_URL + "apibot")
GAMES = {}

# FUTURE TODO - ideally endpoints, game info like squares comes from ontology.

# Main Code
app = Flask(__name__)

@app.route("/dump", methods=["GET"])
def dump():  
    for key in GAMES:
        helper = GAMES[key] 
        print("Game for ", key)
        helper.print_game()
        print("Visual for ", key)
        result = visualize(helper.graph)
        return current_app.send_static_file('visual.png')

    return render_template('dump.html')


def visualize(g):
    stream = io.StringIO()
    rdf2dot(g, stream, opts = {display})
    dg = pydotplus.graph_from_dot_data(stream.getvalue())
    result = dg.write_png("visual.png")
    return result
    #png = dg.create_png()
    #display(Image(png))


# initialise
od = OntDoc(ontology="TicTacToe.owl")

# produce HTML
html = od.make_html()

# Generated using https://github.com/RDFLib/pyLODE
# TODO: this should include some kind of README of how to play
# This needs to point back to index
@app.route("/tic-tac-toe", methods=["GET"])
def info():
    return html

# This needs to point back to index
@app.route("/apibot", methods=["GET"])
def apibot():
    json_response = ResponseWriter(BASE_URL + "apibot","ttt:Agent")
    json_response.add_field("description","basic opponent (no strategy)")
    json_response.add_link(BASE_URL,method_name="GET")
    inpage_json = json_response.build()
    return render_template('apibot.html',json_schema=inpage_json)

# Index points to ontology     /tic-tac-toe
#                 opponent     /apibot
# and form to register to play /register
@app.route('/')
def home():
    # TODO: check if registered
    rw = ResponseWriter("tic-tac-toe","http://localhost:8083")

    rw.add_link(BASE_URL + "tic-tac-toe",method_name="GET")
    rw.add_link(BASE_URL + "apibot",method_name="GET")
       
    id = request.args.get('id')
    if id:
        id = uuid.UUID(id)
        if id in GAMES:
            helper,apibot = GAMES[id] 
            add_links_for_active_game(helper, rw, id)
    else:
        rw.add_form(BASE_URL + "register",method_name="POST",contentType="application/json",op="readproperty")
        rw.add_form_property(BASE_URL + "register","ttt:Agent",False,True)

    inpage_json = rw.build()
    return render_template('index.html',json_schema=inpage_json) #TODO fix this formatting



#GAME FLOW
# Need to annotate with:
# Require agent URL to be posted
# What else? Linked URLs.

# FORM: https://w3c.github.io/wot-thing-description/#form
# "A form can be viewed as a statement of "To perform an operation ]
# type operation on form context, make a request method request to 
# submission target" where the optional form fields may further
#  describe the required request. In Thing Descriptions, the form 
# context is the surrounding Object, such as Properties, Actions, 
# and Events or the Thing itself for meta-interactions."
#Required headers: Content-Type: application/x-www-form-urlencoded
# Example data:
# URL: http://localhost:8083/register?id=1
# Body: agent=http://agentURL/agent
#TODO: get should presumably tell you how to fill in the form
@app.route("/register", methods=["POST"])
def register():  
    # Assign and ID and return it
    id = uuid.uuid4()
    agent_url = request.form['agent']
    agent_opponent = URIRef(agent_url)
    g = Graph()
    g.parse('TicTacToe.owl')
    uri = BASE_URL + 'game/id=' + str(id)
    print(uri)
    game = URIRef(uri)
    helper = GraphHelperMethods(g,'tic-tac-toe',game, API_BOT, agent_opponent,id)
    apibot = APIBOT(API_BOT, helper)
    GAMES[id] = helper,apibot;

    rw = ResponseWriter(BASE_URL + "register","")
    rw.add_link(BASE_URL + "",method_name="GET")
    add_links_for_active_game(helper, rw, id)
    return rw.build()


# /board endpoint returns information about the squares in a game
# if there is a game in progress, otherwise informs the user to register
# Boards points to index     /
#                 result     /result
# and form to play a square  /square
@app.route("/board", methods=["GET"])
def board():
    rw = ResponseWriter(BASE_URL + "board","ttt:Board")
    rw.add_link(BASE_URL + "",method_name="GET")
    id = request.args.get('id')
    id = uuid.UUID(id)
    if id in GAMES:
        helper,apibot = GAMES[id] 
        add_links_for_active_game(helper, rw, id)
        board = helper.get_board()
        for b in board:
            rw.add_field(b,board[b])
        
    else:
        rw.add_error("Not registered")

    return rw.build()
    

def add_links_for_active_game(helper, rw, id):
    id_str = str(id)
    if (helper.is_game_over()):
        rw.add_link(BASE_URL + "result?id=" + id_str,method_name="GET") 
        rw.add_link(BASE_URL + "register",method_name="GET") 
    else:
        rw.add_link(BASE_URL + "board?id=" + id_str,method_name="GET") 
        free_squares = helper.get_free_squares()
        for sq in free_squares:
            sq_str = str(sq)
            square_id = sq_str.split(helper.ttt,1)[1]
            rw.add_link(BASE_URL + square_id + "?id=" + id_str,method_name="POST") 
       


# Result points back to index
@app.route('/result')
def result():
    #Start building response
    rw = ResponseWriter(BASE_URL + "result","ttt:TicTacToeResult")
    id = request.args.get('id')
    id = uuid.UUID(id)
    #Is the player registered 
    if id in GAMES:
        helper,apibot = GAMES[id] 
        id_str = str(id)
        rw.add_link(BASE_URL + "board?id=" + id_str,method_name="GET") 
        winner = helper.get_winner()

        if winner:
            rw.add_field("ttt:TicTacToeResult",winner)
        else:
            rw.add_field("ttt:TicTacToeResult","None") #TODO consider some placeholder, also something for draw

    else:
        rw.add_error("Not registered")


    rw.add_link(BASE_URL + "",method_name="GET")
    return rw.build()



# Not registered? 404 and LINK TO /REGISTER ENDPOINT
# Registered? RETURNS LINKS TO BOARD AND ONTOLOGY
# If no game token in post, given new id / token - this should be to ontology 

# TODO CHECK Required headers: Content-Type: application/x-www-form-urlencoded
@app.route('/Square<sq>', methods=["POST"])
def square(sq):
    rw = ResponseWriter(BASE_URL + "Square"+sq,"ttt:Square"+sq)
    rw.add_link(BASE_URL + "",method_name="GET") #Always link to index page
    id = request.args.get('id')
    id = uuid.UUID(id)
    print(GAMES)
    if id in GAMES:
        id_str = str(id)
        helper,apibot = GAMES[id] 
        rw.add_link(BASE_URL + "board?id=" + id_str,method_name="GET") 

        # Check for invalid posts
        square_uri = helper.get_square_url_for_int(sq)
        if helper.is_square_free(square_uri):
            helper.add_opponent_move(square_uri) #TODO What is the move is invalid?
            helper.print_game() #TODO What should this do instead
        
            #Is there a winner
            game_over = helper.is_game_over()
            if game_over:
                #Make the result URL available
                print("We have a result (after agent move)")
                rw.add_link(BASE_URL + "result?id=" + id_str,method_name="GET") 
            else:
                #Now API Bot's turn
                if apibot.make_move():
                    #Turn made, there is already a link to the board
                    game_over = helper.is_game_over()
                    if game_over:
                        print("We have a result (after apibot move)")
                        rw.add_link(BASE_URL + "result?id=" + id_str,method_name="GET") 
                else:
                    #It was a Draw: make the result URL available TODO: this code should never be called
                    print('The game is a draw')
                    rw.add_link(BASE_URL + "result?id=" + id_str,method_name="GET") 
        else:
             rw.add_error("Invalid move")
              
    else: 
        rw.add_error("Not registered")
    
    return rw.build()

 
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=PORT)

