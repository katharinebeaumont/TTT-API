import sys
import json
from flask import Flask,request,Response,render_template,current_app
from rdflib import Graph, URIRef
from graphhelpermethods import GraphHelperMethods
from pylode import OntDoc
import uuid
import io
import pydotplus
from IPython.display import display, Image
from rdflib.tools.rdf2dot import rdf2dot
from flask import Response
from constants import HOST, PORT, BASE_URL, BOT_NAME, API_BOT_URI, GAME_ONTOLOGY, GAME_ONTOLOGY_TAG, GAME_ONTOLOGY_PREFIX


from responsewriter import ResponseWriter
from apibot import APIBOT

GAMES = {}

# Main Code
app = Flask(__name__)


### Routes ###


# /
# If not registered
#   Form to:        /register
#   APIBOT RDF in the form of 
#   GAME_ONTOLOGY_PREFIX + ":Agent" : APIBOT URI
# If registered
#   Links and forms to active game (see function add_links_for_active_game) 
@app.route('/')
def home():
    rw = ResponseWriter(BASE_URL,GAME_ONTOLOGY_PREFIX + ":Game")

    id = request.args.get('id')
    if id:
        id = uuid.UUID(id)
        if id in GAMES:
            helper,apibot = GAMES[id] 
            add_links_for_active_game(helper, rw, id)
    else:
        rw.add_form(BASE_URL + "register",method_name="POST",contentType="application/json",op="readproperty")
        rw.add_form_property(BASE_URL + "register","@id",False,True)


    rw.add_field(GAME_ONTOLOGY_PREFIX + ":Agent", API_BOT_URI)
    return format_response(rw)


# /tic-tac-toe
# HOSTING THE ONTOLOGY
# Generated using https://github.com/RDFLib/pyLODE
# initialise
od = OntDoc(ontology=GAME_ONTOLOGY)

# produce HTML
html = od.make_html()

# Route returns html, unlike other routes, which return JSON
@app.route("/" + GAME_ONTOLOGY_TAG, methods=["GET"])
def info():
    return html

# /apibot
# APIBOT INFORMATION
# Route returns html, unlike other routes, which return JSON
@app.route("/" + BOT_NAME, methods=["GET"])
def apibot():
    json_response = ResponseWriter(BASE_URL + BOT_NAME,GAME_ONTOLOGY_PREFIX + ":Agent")
    json_response.add_field("description","basic opponent (no strategy)")
    json_response.add_link(BASE_URL,method_name="GET")
    inpage_json = json_response.build()
    # TODO change to not be html
    return render_template('apibot.html',json_schema=inpage_json)


# /register
# This is a form
#   FORM: https://w3c.github.io/wot-thing-description/#form
#   "A form can be viewed as a statement of "To perform an operation ]
#   type operation on form context, make a request method request to 
#   submission target" where the optional form fields may further
#   describe the required request. In Thing Descriptions, the form 
#   context is the surrounding Object, such as Properties, Actions, 
#   and Events or the Thing itself for meta-interactions."
#   Example data:
#   Body: 
#   {
#       "@id": "http://agentURL.com",
#       "@type":GAME_ONTOLOGY_PREFIX + ":Agent",
#       "@context": {
#           "ttt": "http://localhost:8083/tic-tac-toe#"
#       }
#   }
#
#   Links to:     /
#   Links and forms to active game (see function add_links_for_active_game) 
@app.route("/register", methods=["POST"])
def register():  
    # Assign an ID for the game
    id = uuid.uuid4()

    # Get the opponent name from the request body
    body = request.get_json()
    agent_url = body['@id']
    agent_opponent_uri = URIRef(agent_url)

    # Create a new RDF graph for the game using the tic-tac-toe ontology
    g = Graph()
    g.parse(GAME_ONTOLOGY)
    helper = GraphHelperMethods(g, GAME_ONTOLOGY_TAG, BASE_URL, API_BOT_URI, agent_opponent_uri, id)
    apibot = APIBOT(API_BOT_URI, helper)
   
    # Store the game helper (access to RDF graph) and the opponent instance against the game ID
    GAMES[id] = helper,apibot;
    # Routine memory check (this object gets large...)
    #if (GAMES):
     #   objectSize = sys.getsizeof(GAMES);
      #  if (objectSize > 10000):
          #  print("Flushing GAMES")
       ##     print("GAMES object is too big! ", objectSize)
           # d GAMES[id] = helper,apibot;
         ##   GAMES = {}
    
    # Write the response
    rw = ResponseWriter(BASE_URL + "register","")
    rw.add_link(BASE_URL + "",method_name="GET")
    add_links_for_active_game(helper, rw, id)

    return format_response(rw)


# /Board 
# 
# If not registered
#   Links to:       /
# If registered
#   Links and forms to active game (see function add_links_for_active_game) 
#   Board RDF in the form of (for example)
#   "ttt:Board" : board URl
#   "ttt:hasSquare": {
#                "http://localhost:8083/Square12?id=6b1bef0d-5211-4a01-8ba5-78b0480ffd4f": {
#                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://localhost:8083/tic-tac-toe#Square12",
#                    "http://localhost:8083/tic-tac-toe#moveTakenBy": "http://localhost:8083/apibot"
#            }    
#   }
@app.route("/Board", methods=["GET"])
def board():
    rw = ResponseWriter(request.url,GAME_ONTOLOGY_PREFIX + ":Board")
    rw.add_link(BASE_URL + "",method_name="GET")
    id = request.args.get('id')
    id = uuid.UUID(id)
    if id in GAMES:
        helper,apibot = GAMES[id] 
        add_links_for_active_game(helper, rw, id) #This adds links to free squares
        board = helper.get_board_occupied()
        for b in board:
            rw.add_nested_field(GAME_ONTOLOGY_PREFIX + ":hasSquare",b,board[b]) #Just passing key in 

    else:
        rw.add_error("Not registered")

    return format_response(rw)
    

# /result
#
# If registered
#   Links to      /Board
#                 / 
#   Result RDF in the form of (for example)
#       GAME_ONTOLOGY_PREFIX + ":TicTacToeResult" : agent_url OR "None" (draw)
# Else
#   Error and link to index
@app.route('/result')
def result():
    #Start building response
    rw = ResponseWriter(request.url,GAME_ONTOLOGY_PREFIX + ":TicTacToeResult")
    id = request.args.get('id')
    id = uuid.UUID(id)
    #Is the player registered 
    if id in GAMES:
        helper,apibot = GAMES[id] 
        rw.add_link(helper.board,method_name="GET") 
        winner = helper.get_winner()
       
        if winner:
            rw.add_field(GAME_ONTOLOGY_PREFIX + ":TicTacToeResult",winner)
        else:
            rw.add_field(GAME_ONTOLOGY_PREFIX + ":TicTacToeResult","None") #TODO consider some placeholder, also something for draw

        # Save game
        try:
            helper.save_graph()
        except:
            print("An exception occurred saving the graph")

        # Remove value from GAMES dictionary #keepItClean
        del GAMES[id]

    else:
        rw.add_error("Not registered")


    rw.add_link(BASE_URL + "",method_name="GET")
   

    return format_response(rw)


# /Square<sq>
#
# E.g. /Square11, /Square12... /Square33
# This is a form
# ...with no body
# 
# If registered
#   Links to      /Board
#                 / 
#   Information on move taken by e.g.
#   GAME_ONTOLOGY_PREFIX + ":moveTakenBy": "http://agentURL.com",
#   If game over
#       Links to      /result
#   If the move is invalid
#       Provides error
# Else
#   Error and link to index
@app.route('/Square<sq>', methods=["PUT"])
def square(sq):

    rw = ResponseWriter(request.url,GAME_ONTOLOGY_PREFIX + ":Square"+sq) #TODO this should be the full url
    rw.add_link(BASE_URL + "",method_name="GET") #Always link to index page
    id = request.args.get('id')
    id = uuid.UUID(id)
    if id in GAMES:
        id_str = str(id)
        helper,apibot = GAMES[id] 
        rw.add_field(GAME_ONTOLOGY_PREFIX + ":moveTakenBy", helper.oagent)
        
        rw.add_link(helper.board,method_name="GET") 
        # Check for invalid posts
        if helper.is_square_free(request.url):
            helper.add_opponent_move(request.url) #TODO What is the move is invalid?
            
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
    
    return format_response(rw)


### Helper methods ###


# Game over?
# Links to:    /result
# Forms to:    /register
# Otherwise
# Links to:    /Board
# Forms to:    /Square<SquareId>    (all free squares)
def add_links_for_active_game(helper, rw, id):
    id_str = str(id)
    if (helper.is_game_over()):
        rw.add_link(BASE_URL + "result?id=" + id_str,method_name="GET") 
        rw.add_form(BASE_URL + "register",method_name="POST",contentType="application/json",op="readproperty")
        rw.add_form_property(BASE_URL + "register",GAME_ONTOLOGY_PREFIX + ":Agent",False,True)
    else:
        board = helper.board
        rw.add_link(board,method_name="GET") 
        free_squares = helper.get_free_squares()
        for sq in free_squares:
            rw.add_form(str(sq),method_name="PUT",contentType="application/json",op="readproperty") 
            

# Write the response object 
def format_response(rw):
    response_json = rw.build()
    json_str = json.dumps(response_json);
    return Response(json_str, mimetype='application/ld+json')


# Just don't use this for now... Huge memory drain, very slow, not particularly useful. Look at the 
# ttl files in the results folder instead
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


# ...Really, don't!!!! 
def visualize(g):
    stream = io.StringIO()
    rdf2dot(g, stream, opts = {display})
    dg = pydotplus.graph_from_dot_data(stream.getvalue())
    result = dg.write_png("visual.png")
    return result
    #png = dg.create_png()
    #display(Image(png))


# Start the server
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=PORT)

