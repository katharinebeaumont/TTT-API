import pytest
from app import app
import json

# container object for test applications #
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# End-to-end app tests 
class TestApp:

    def checkID(self, data_Json, expected_ID):
        assert data_Json["@id"] == expected_ID
        

    def checkType(self, data_Json, expected_type):
        assert data_Json["@type"] == expected_type


    def checkContext(self, data_Json):
        assert data_Json["@context"]["@vocab"] ==  'https://www.w3.org/2019/wot/hypermedia#'
        assert data_Json["@context"]["ttt"] == 'http://localhost:8083/tic-tac-toe#'
        assert data_Json["@context"]["htv"] == 'http://www.w3.org/2011/http#'
        assert data_Json["@context"]["wot"] == 'https://w3c.github.io/wot-thing-description/#'
        assert data_Json["@context"]['sch'] == 'https://schema.org/'
        assert data_Json["@context"]['links']["@id"] == 'Link'
        assert data_Json["@context"]['forms']["@id"] == 'Form'
        assert data_Json["@context"]['href']["@id"] == 'hasTarget'
        assert data_Json["@context"]['rel']['@id'] == 'hasRelationType'
        assert data_Json["@context"]['rel']['@type'] == '@vocab'


    def checkForm(self, data_Json, expected_href, expected_contentType, expected_methodName, expected_op):
        assert data_Json["href"] == expected_href
        assert data_Json["contentType"] == expected_contentType
        assert data_Json["htv:methodName"] == expected_methodName
        assert data_Json["wot:op"] == expected_op
            

    def checkLink(self, data_Json, expected_href, expected_methodName):
        assert data_Json["href"] == expected_href
        assert data_Json["htv:methodName"] == expected_methodName


    def extractID(self, json):
        url_string = json["href"]
        print(url_string)
        return url_string.split("id=",1)[1]


    def checkSquareForms(self, data_Json, squares, id):
        square_index = 0
        for innerObj in data_Json:
            self.checkForm(innerObj,  'http://localhost:8083/Square' + str(squares[square_index]) + "?id=" + id, 'application/json', 'PUT', 'readproperty')
            square_index = square_index + 1
            #Using for loop checks there are no other forms other than squares
        
        assert square_index == len(squares)
        #And that all the squares were checked

    # Check ID, Type, Context and then the links and forms
    def test_index(self, client):
        res = client.get('/')
        assert res.status_code == 200
        data = res.get_data()
        data_Json = json.loads(data)
       
        self.checkID(data_Json,'http://localhost:8083/')
        self.checkType(data_Json,'ttt:Game')
        self.checkContext(data_Json)

        assert data_Json["ttt:Agent"] == 'http://localhost:8083/apibot'
       
        for innerObj in data_Json["forms"]:
            self.checkForm(innerObj,  'http://localhost:8083/register', 'application/json', 'POST', 'readproperty')
            for properties in innerObj["properties"]:
                assert properties["name"] == "@id"
                assert properties["readOnly"] == False
                assert properties["required"] == True

            #Using for loop checks there are no other forms other than registration
           
        #How check there is "nothing else" in the response object?
        # Should not have any links
    
    def test_register(self, client):
        res = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        assert res.status_code == 200
        
        self.checkID(res.json, "http://localhost:8083/register")
        self.checkType(res.json, "")
        #Should have links to index and the board, with the game id
        self.checkLink(res.json["links"][0], "http://localhost:8083/", "GET")
        id = self.extractID(res.json["links"][1])
        self.checkLink(res.json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")
        data_Json = res.json
        #Now check forms contain all squares in order
        squares = [11,12,13,21,22,23,31,32,33]
        self.checkSquareForms(data_Json["forms"], squares, id)
        

    def test_index_registered(self, client):
        res = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        id = self.extractID(res.json["links"][1])
        self.checkLink(res.json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")

        res = client.get('/?id=' + id)
        assert res.status_code == 200
        data = res.get_data()
        data_Json = json.loads(data)
       
        self.checkID(data_Json,'http://localhost:8083/')
        self.checkType(data_Json,'ttt:Game')
        self.checkContext(data_Json)

        assert data_Json["ttt:Agent"] == 'http://localhost:8083/apibot'

        #Now we should have links for active games, i.e. all squares, board
        # Should have link to board
        id = self.extractID(data_Json["links"][0])
        self.checkLink(data_Json["links"][0], "http://localhost:8083/Board?id=" + id, "GET")
        # Should have forms to squares, and should not have a form to register
        squares = [11,12,13,21,22,23,31,32,33]
        self.checkSquareForms(data_Json["forms"], squares, id)
        
       
    def test_register_twice(self, client):
        # Should start two games, giving two different ids
        res = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        id = self.extractID(res.json["links"][1])
        self.checkLink(res.json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")

        res = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        id2 = self.extractID(res.json["links"][1])
        self.checkLink(res.json["links"][1], "http://localhost:8083/Board?id=" + id2, "GET")
        assert id != id2


    def test_square_form(self, client):
        # Should start a game, 
        res = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        # Get the link to a square
        assert res.status_code == 200
        data = res.get_data()
        data_Json = json.loads(data)
        # first square form should be 11
        square_form = data_Json["forms"][0]["href"]
        #get everything after localhost:8083
        
        link = square_form.split("8083/",1)[1]
        print("LINK " + link)
        res = client.put(link)
        assert res.status_code == 200

        data = res.get_data()
        data_Json = json.loads(data)
        
        #self.checkID(data_Json,square_form) #TODO WHY is there no port in this put request, but there is for get and post
        assert data_Json["@id"] == 'http://localhost/' + link

        self.checkType(data_Json,'ttt:Square11')
        self.checkContext(data_Json)

        assert data_Json["ttt:moveTakenBy"] == "http://agentURL.com"
        # Should be no forms (so get a KeyError)
        with pytest.raises(KeyError):
            data_Json["forms"] 

        #Should only be 2 links, board and index
        assert len(data_Json["links"]) == 2
        self.checkLink(data_Json["links"][0], "http://localhost:8083/", "GET")
        id = self.extractID(data_Json["links"][1])
        self.checkLink(data_Json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")


    def test_board_no_moves(self, client):
        # Should start two games, giving two different ids
        res = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        id = self.extractID(res.json["links"][1])
        self.checkLink(res.json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")

        res = client.get("Board?id=" + id)
        assert res.status_code == 200
        data = res.get_data()
        data_Json = json.loads(data)
        
        # Check id, type, context
        self.checkID(data_Json,"http://localhost/Board?id=" + id)
        self.checkContext(data_Json)
        self.checkType(data_Json,"ttt:Board")

        # Shouldn't have any squares yet
        with pytest.raises(KeyError):
            data_Json["ttt:hasSquare"] 

        # Link to index
        assert len(data_Json["links"]) == 1
        self.checkLink(data_Json["links"][0], "http://localhost:8083/", "GET")

        # Should have forms to all squares, and should not have a form to register
        squares = [11,12,13,21,22,23,31,32,33]
        self.checkSquareForms(data_Json["forms"], squares, id)


    def test_board_made_one_move(self, client):
        res_register = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        data_register = res_register.get_data()
        data_register = json.loads(data_register)
        # first square form should be 11
        # Get square form from /register response
        square_form = data_register["forms"][0]["href"]
        
        link = square_form.split("8083/",1)[1]
        # PUT to square form 
        res_square = client.put(link)
        assert res_square.status_code == 200
        # Not expecting any errors
        with pytest.raises(KeyError):
            res_square.json["sch:error"]
        
        assert res_square.json["ttt:moveTakenBy"] == "http://agentURL.com"
        
        #Check links to index and board
        self.checkLink(res_square.json["links"][0], "http://localhost:8083/", "GET")
        id = self.extractID(res_square.json["links"][1])
        self.checkLink(res_square.json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")
        
        # GET board response
        res_board = client.get("Board?id=" + id)
        assert res_board.status_code == 200
        data_board = res_board.get_data()
        data_board = json.loads(data_board)
        
        # Check id, type, context
        self.checkID(data_board,"http://localhost/Board?id=" + id)
        self.checkContext(data_board)
        self.checkType(data_board,"ttt:Board")

        # Link to index only
        assert len(data_board["links"]) == 1
        self.checkLink(data_board["links"][0], "http://localhost:8083/", "GET")

        # Should have forms to all squares except Square11,and Square12 (as APIBOT has made this move) and should not have a form to register
        squares = [13,21,22,23,31,32,33]
        print(data_board)
        self.checkSquareForms(data_board["forms"], squares, id)

        # Should have two results for hasSqaure, 
        assert len(data_board["ttt:hasSquare"] ) == 2


    def test_board_cannot_repeat_move(self, client):
        # Start a game
        res_register = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        data_register = res_register.get_data()
        data_register = json.loads(data_register)
        # first square form should be 11
        # Get square form from /register response
        square_form = data_register["forms"][0]["href"]
        
        link = square_form.split("8083/",1)[1]
        # PUT to square form 
        res_square = client.put(link)
        assert res_square.status_code == 200
        # Not expecting any errors
        with pytest.raises(KeyError):
            res_square.json["sch:error"]
        
        assert res_square.json["ttt:moveTakenBy"] == "http://agentURL.com"
        
        #Attempt to PUT to square form again
        res_square = client.put(link)
        assert res_square.status_code == 200
        # Not expecting any errors
        assert res_square.json["sch:error"] == "Invalid move"


    def test_board_result_page(self, client):
        res_register = client.post('register', json={
                "@id": "http://agentURL.com",
                "@type": "ttt:Agent",
                "@context": {
                    "ttt": "http://localhost:8083/tic-tac-toe#"
            }})
        
        data_register = res_register.get_data()
        data_register = json.loads(data_register)
        # first square form should be 11
        # Get square form from /register response
        square_form = data_register["forms"][0]["href"]
        
        link = square_form.split("8083/",1)[1]
        # PUT to square form 11
        res_square = client.put(link)
        assert res_square.status_code == 200
        # Not expecting any errors
        with pytest.raises(KeyError):
            res_square.json["sch:error"]
        
        assert res_square.json["ttt:moveTakenBy"] == "http://agentURL.com"
        
        #Get the board, get links - assume APIBot strategy is to take next free 
        # square (12) - FIXME: these tests will break if have a different bot strategy
        id = self.extractID(res_square.json["links"][1])
        self.checkLink(res_square.json["links"][1], "http://localhost:8083/Board?id=" + id, "GET")
        
        # PUT to square form 21
        res_square = client.put("Square21?id=" + id)
        assert res_square.status_code == 200
         # Not expecting any errors
        with pytest.raises(KeyError):
            res_square.json["sch:error"]
        # ... and 31
        res_square = client.put("Square31?id=" + id)
        assert res_square.status_code == 200
         # Not expecting any errors
        with pytest.raises(KeyError):
            res_square.json["sch:error"]
        
        data = res_square.json 
        # Now should have link to index, results and board
        assert len(res_square.json["links"]) == 3 
        self.checkLink(data["links"][0], "http://localhost:8083/", "GET")
        self.checkLink(data["links"][1], "http://localhost:8083/Board?id=" + id, "GET")
        self.checkLink(data["links"][2], "http://localhost:8083/result?id=" + id, "GET")
        # Should not have any forms
        with pytest.raises(KeyError):
            data["forms"] 

        # Get the results link
        results = client.get("result?id=" + id)
        data = results.json

        # Result should be agent url
        assert data["ttt:TicTacToeResult"] == "http://agentURL.com"
        # Links to board and index, no forms
        assert len(data["links"]) == 2
        self.checkLink(data["links"][1], "http://localhost:8083/", "GET")
        self.checkLink(data["links"][0], "http://localhost:8083/Board?id=" + id, "GET")
        
        with pytest.raises(KeyError):
            data["forms"] 

