from rdflib import Graph, Literal, URIRef, Namespace, RDF, RDFS, OWL
from rdflib.namespace import NamespaceManager

class RDFStore():

    def __init__(self, graph, prefix, url, xagentplayer, oagentplayer, id):
        self.graph = graph
        self.xagent = xagentplayer
        self.oagent = oagentplayer
        id = str(id)
        self.id = id
        ns_wtm = ''
        for ns_prefix, namespace in self.graph.namespaces():
            if prefix == ns_prefix:
                ns_wtm = namespace

        n = Namespace(ns_wtm)
        nm = self.graph.namespace_manager
        nm.bind(prefix, n)
        self.ttt = n
       
        #Assign player roles
        self.graph.add((xagentplayer, RDF.type, self.ttt.XPlayerRole))
        self.graph.add((oagentplayer, RDF.type, self.ttt.OPlayerRole))

        #Create Game instance
        game_instance = URIRef(url + "Game?id="+id)
        self.game = game_instance
       
        self.graph.add((game_instance, RDF.type, OWL.NamedIndividual))
        self.graph.add((game_instance, RDF.type, self.ttt.Game))
        self.graph.add((game_instance, self.ttt.hasID, Literal(id)))
        
        self.graph.add((game_instance, self.ttt.providesAgentRole, xagentplayer))
        self.graph.add((game_instance, self.ttt.providesAgentRole, oagentplayer))
        
        #Create Board instance
        board_instance = URIRef(url + "Board?id="+id)
        self.board = board_instance
        self.graph.add((board_instance, RDF.type, OWL.NamedIndividual))
        self.graph.add((board_instance, RDF.type, self.ttt.Board))

        for (s, p, o) in self.graph.triples((None, RDFS.subClassOf, self.ttt.Square)):
            square_itself = s
            square_number_string = str(s)
            square_superclass_string = str(self.ttt.Square)
            square_int = square_number_string.split(square_superclass_string,1)[1]
            # Everything after self.ttt.Square 
            #Need to create instances of the square classes,
            square_url = url + "Square"+str(square_int)+"?id="+id
            square_instance = URIRef(square_url)
            self.graph.add((square_instance, RDF.type, OWL.NamedIndividual ))
            self.graph.add((square_instance, RDF.type, square_itself))
            #add them to the board
            self.graph.add((board_instance, self.ttt.hasSquare, square_instance))

    
    def save_graph(self):
        self.graph.serialize(destination="results/" + self.id + ".ttl")


    def get_first_move(self):
        # Get first move, then go to next move
        if (self.game, self.ttt.firstMove, None) in self.graph:
            for s, p, o in self.graph.triples((self.game, self.ttt.firstMove, None)):
                # Should only be one
                return o
            #Or there isn't one yet
        return None


    def get_next_move(self, square):
        return self.graph.value(square,  self.ttt.nextMove)
    

    def get_last_move(self):
        # Get first move, then go to next move
        firstSquare = self.get_first_move()
        if not firstSquare:
            return None
        
        nextSquare = self.get_next_move(firstSquare)
        if not nextSquare:
            return firstSquare
        
        finalSquare = False
        #Using first square, get next move until there
        # aren't anymore
        while (nextSquare):
            finalSquare = nextSquare
            nextSquare = self.get_next_move(nextSquare)


        return finalSquare


    def add_move(self, square, agent):
        if not self.get_first_move(): 
            self.graph.add((self.game,  self.ttt.firstMove, square))
        else: #Otherwise there is a previous move
            latestSquare = self.get_last_move()
            self.graph.add((latestSquare, self.ttt.nextMove, square))
        
        self.graph.add((square,  self.ttt.moveTakenBy, agent))
        self.graph.add((square,  self.ttt.subEventOf, self.game))


    def add_opponent_move(self, square):
        self.add_move(square, self.oagent)


    def square_instance_to_square(self, square_instance):
        for (s, p, o) in self.graph.triples((square_instance, RDF.type, None)):
            #ignore if o is namedIndividual
            if (o != OWL.NamedIndividual):
                return o


    def square_to_square_instance(self, square):
        for (s, p, o) in self.graph.triples((None, RDF.type, square)):
            return s


    def square_instance_from_number(self, num):
        for (s, p, o) in self.graph.triples((None, RDFS.subClassOf, self.ttt.Square)):
            square_itself = s # I.e. Square11
            if num in str(square_itself):
                return self.square_to_square_instance(square_itself)
            

    def get_winner(self):

        player_1 = {}
        player_2 = {}
        # Get the occupied squares
        squares = self.get_occupied_squares()
        # Split into two dicts to check
        for sq in squares:
            agent = squares[sq]
            #Convert square instance into square int
            square_class = self.square_instance_to_square(sq)
            if agent in player_1:
                player_1[agent] = player_1[agent] + [square_class]
            elif agent in player_2:
                player_2[agent] = player_2[agent] + [square_class]
            elif len(player_1) == 0:
                player_1[agent] = [square_class]
            else:
                player_2[agent] = [square_class]         
        
        for agent in player_1:
            if (self.check_for_win(player_1[agent])):
                return agent

        for agent in player_2:
            if (self.check_for_win(player_2[agent])):
                return agent
        
        return None
    
    def check_for_win(self, squares_list):
        if (len(squares_list)<2):
            return False
        
        #Left to right diagonal
        #Right to left diagonal
        #Row 1 - 3
        #Col 1 - 3
        # If 11, see if have 12, 13
        # or 11, 21, 31
        # or 11, 22, 33
        if self.ttt.Square11 in squares_list:
            if self.ttt.Square12 in squares_list and self.ttt.Square13 in squares_list:
                return True
            if self.ttt.Square21 in squares_list and self.ttt.Square31 in squares_list:
                return True
            if self.ttt.Square22 in squares_list and self.ttt.Square33 in squares_list:
                return True
        
        if self.ttt.Square12 in squares_list:
            if self.ttt.Square22 in squares_list and self.ttt.Square32 in squares_list:
                return True

        if self.ttt.Square13 in squares_list:
            if self.ttt.Square23 in squares_list and self.ttt.Square33 in squares_list:
                return True
            if self.ttt.Square22 in squares_list and self.ttt.Square31 in squares_list:
                return True

        if self.ttt.Square21 in squares_list:
            if self.ttt.Square22 in squares_list and self.ttt.Square23 in squares_list:
                return True

        if self.ttt.Square31 in squares_list:
            if self.ttt.Square32 in squares_list and self.ttt.Square33 in squares_list:
                return True

        return False
    

    def is_game_over(self):
        w = self.get_winner()
        if w:
            return True
        else:
            sq = self.get_free_squares()
            if (len(sq) > 0):
                return False
            return True
    

    def is_square_free(self, square_url):
        if self.is_game_over():
            return False
        
        free_squares = self.get_free_squares()
        square_url_id = 'Square' + str(square_url).split("/Square",1)[1]
        for free_square_url in free_squares:
            # Get the Square ID ... doing this because the tests set the request URL as 
            # localhost/Square11?id=... instead of localhost:8083/Square11?id=..
            free_square_id = 'Square' + str(free_square_url).split("/Square",1)[1]
            if free_square_id == square_url_id:
                return True
        if square_url in free_squares:
            return True
        
        return False
    

    ##
    # This should be in the form
    # Board hasSquare Square_url (square in gameplay)
    # Square_url isType Square11 etc
    # Square_url moveTakenBy XPlayerRole
    ##
    def get_board_occupied(self):

        board = {}
        
        occupied_squares = self.get_occupied_squares()
        for key in occupied_squares:
            square_instance = key
            agent = occupied_squares[key]
            square_class = self.square_instance_to_square(square_instance)
            board[square_instance] = { RDF.type : square_class, self.ttt.moveTakenBy : agent }

        return board
    

    def get_occupied_squares(self):
        
        a = self.graph.query("""
        SELECT ?s ?p
        WHERE {
            ?s rdf:type owl:NamedIndividual ;
               rdf:type [rdfs:subClassOf tic-tac-toe:Square] ;
                tic-tac-toe:moveTakenBy ?p .
        }
        """)

        squares = {}         
        for row in a:
            squares[row['s']]=row['p']
        
        return squares
    


    def get_free_squares(self):
        a = self.graph.query("""
        SELECT ?s
        WHERE {
            ?s rdf:type owl:NamedIndividual ;
               rdf:type [rdfs:subClassOf tic-tac-toe:Square] .
            FILTER NOT EXISTS { ?s tic-tac-toe:moveTakenBy ?p }
        }
        """)

        squares = []         
        for row in a:
            #print(row['s'])
            squares.append(row['s'])
        
        return squares
    

    def print_game(self):
        #1. Get squares
        #Want print out like this:
        # O Player: URL
        # X Player: URL
        # Game ID: URL
        # - X -
        # O - -
        # - X -
        print("*GAME:* " + self.game)
        for (s, p, o) in self.graph.triples((None, RDF.type, self.ttt.XPlayerRole)):
            print("X Player Role: " + s)
        for (s, p, o) in self.graph.triples((None, RDF.type, self.ttt.OPlayerRole)):
            print("O Player Role: " + s)
        
        print("*board:*")
        # Get the squares
        row1, row2, row3 = self.get_board_visual() 
        print(row1)
        print(row2)
        print(row3)

    
    def get_board_visual(self):
        row1 = ""   
        row1 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square11), row1)
        row1 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square12), row1)
        row1 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square13), row1)
        row2 = ""   
        row2 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square21), row2)
        row2 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square22), row2)
        row2 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square23), row2)
        row3 = ""   
        row3 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square31), row3)
        row3 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square32), row3)
        row3 = self.get_square_desc(self.square_to_square_instance(self.ttt.Square33), row3)
        return row1, row2, row3
    

    def get_square_desc(self, square, row_desc):
        square_filled = False;    
        for (s, p, o) in self.graph.triples((square, self.ttt.moveTakenBy, None)):
            square_filled = o
            #Is o X or O player Role?
            playerRole = self.graph.value(o, RDF.type)
            if (playerRole == self.ttt.XPlayerRole):
                row_desc += "X "
            else:
                row_desc += "O "

        if not square_filled:
            row_desc += "- "
        return row_desc
    

    def get_graph(self):
        return self.graph