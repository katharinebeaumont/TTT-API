
import unittest
from responsewriter import ResponseWriter
import json
from rdflib import Graph, URIRef, Namespace, RDF, Literal
from rdflib.namespace import NamespaceManager

from graphhelpermethods import GraphHelperMethods

class TestResponseWriter(unittest.TestCase):

    apiBot = URIRef("http://localhost:8083/apibot")
    agentZero = URIRef("http://localhost:7070/agentzero")
    tttgame = URIRef("http://localhost:8083/game/id=1")
    
    def setUp(self):
        
        # Setup 
        g = Graph()
        g.parse('TicTacToe.owl')
        self.helper = GraphHelperMethods(g,'tic-tac-toe',self.tttgame, self.apiBot, self.agentZero, Literal("someId"))
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square11, self.apiBot)


    # Test - basic
    def test_basic(self):
        rw = ResponseWriter("http://localhost:8083")
        rw.add_link("http://localhost:8083/dump","rdfs:seeAlso")
        b = rw.build()
        print(json.dumps(b, indent=4))


    # Test - index page, not registered (link to register form)
    def test_index_page(self):
        rw = ResponseWriter("http://localhost:8083")
        rw.add_link("http://localhost:8083/tic-tac-toe",method_name="GET")
        rw.add_link("http://localhost:8083/apibot",method_name="GET")
        rw.add_link("http://localhost:8083/register",method_name="GET")
        rw.add_form("http://localhost:8083/register",method_name="POST",contentType="application/json",op="readproperty")
        b = rw.build()
        print(json.dumps(b, indent=4))


    # Test - index page, registered
    def test_index_page_registered(self):
        rw = ResponseWriter("http://localhost:8083/")
        rw.add_field("ttt:Game",{"ttt:hasID":self.helper.id})
        rw.add_link("http://localhost:8083/tic-tac-toe",method_name="GET")
        rw.add_link("http://localhost:8083/apibot",method_name="GET")
        rw.add_link("http://localhost:8083/register",method_name="GET")
        rw.add_link("http://localhost:8083/result",method_name="GET")
        rw.add_link("http://localhost:8083/board",method_name="GET")
        rw.add_form("http://localhost:8083/square",method_name="POST",contentType="application/json",op="readproperty")
        b = rw.build()
        print(json.dumps(b, indent=4))
    

    # Test - apibot page (includes information in JSON)
    def test_apibot_page(self):
        rw = ResponseWriter("http://localhost:8083/apibot","ttt:Agent")
        rw.add_field("description","basic opponent (no strategy)")
        rw.add_link("http://localhost:8083/index",method_name="GET")
        b = rw.build()
        print(json.dumps(b, indent=4))
    

    # Test - result response TODO think about this in ontology
    def test_result_page(self):
        rw = ResponseWriter("http://localhost:8083/result","ttt:TicTacToeResult")
        rw.add_field("ttt:TicTacToeResult","ttt:XPlayerRole")
        rw.add_link("http://localhost:8083/index",method_name="GET")
        b = rw.build()
        print(json.dumps(b, indent=4))
    
    
    # Test - result page, not registered
    def test_result_page_not_registered(self):
        rw = ResponseWriter("http://localhost:8083/result","ttt:TicTacToeResult")
        rw.add_error("Not registered")
        rw.add_link("http://localhost:8083/index",method_name="GET")
        b = rw.build()
        print(json.dumps(b, indent=4))
    

    # Test - board response
    def test_board_page(self):
        rw = ResponseWriter("http://localhost:8083/board","ttt:Board")
        
        #TODO: add keyword in ontology for board to group this better
        # apprieviate full url of squares to ttt:
        board = self.helper.get_board()
        for b in board:
            
            rw.add_field(b,board[b])
        
        
        rw.add_link("http://localhost:8083/index",method_name="GET")
        b = rw.build()
        print(json.dumps(b, indent=4))


    def test_form(self):
        rw = ResponseWriter("http://localhost:8083/register")
        rw.add_form("http://localhost:8083/register",method_name="POST",contentType="application/json",op="readproperty")
        rw.add_form_property("http://localhost:8083/register","ttt:Agent",False,True)
        b = rw.build()
        print(json.dumps(b, indent=4))
    # Test - square form response

    # Test - square response
