from rdflib import Graph, Literal, URIRef, Namespace, RDF, RDFS
from rdflib.namespace import NamespaceManager

class GraphHelperMethods():

    def __init__(self, graph, prefix, game, xagentplayer, oagentplayer, id):
        self.graph = graph
        self.game = game
        self.xagent = xagentplayer
        self.oagent = oagentplayer
        self.id = id
        ns_wtm = ''
        for ns_prefix, namespace in self.graph.namespaces():
            if prefix == ns_prefix:
                ns_wtm = namespace

        n = Namespace(ns_wtm)
        nm = self.graph.namespace_manager
        nm.bind(prefix, n)
        self.ttt = n
       
        self.graph.add((xagentplayer, RDF.type, self.ttt.XPlayerRole))
        self.graph.add((oagentplayer, RDF.type, self.ttt.OPlayerRole))

        self.graph.add((game, RDF.type, self.ttt.Game))
        self.graph.add((game, self.ttt.hasID, Literal(id)))
        
        self.graph.add((game, self.ttt.providesAgentRole, xagentplayer))
        self.graph.add((game, self.ttt.providesAgentRole, oagentplayer))
        
    
    def get_square_url_for_int(self, sq_int):
        for sq, p, o in self.graph.triples((None, RDFS.subClassOf, self.ttt.Square)):
            squ_string = str(sq)
            if squ_string.endswith(str(sq_int)):
                return sq


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
        #If there is no first move, this is it
        if not self.get_first_move(): 
            self.graph.add((self.game,  self.ttt.firstMove, square))
        else: #Otherwise there is a previous move
            latestSquare = self.get_last_move()
            self.graph.add((latestSquare, self.ttt.nextMove, square))
        
        self.graph.add((square,  self.ttt.moveTakenBy, agent))
        self.graph.add((square,  self.ttt.subEventOf, self.game))
         

    def add_opponent_move(self, square):
        self.add_move(square, self.oagent)


    def get_winner(self):

        #Left to right diagonal
        #Right to left diagonal
        #Row 1 - 3
        #Col 1 - 3
        a = self.graph.query("""
        SELECT ?winner
        WHERE {
            {tic-tac-toe:Square11 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square22 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square33 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square13 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square22 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square31 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square11 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square12 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square13 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square21 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square22 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square23 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square31 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square32 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square33 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square11 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square21 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square31 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square12 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square22 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square32 tic-tac-toe:moveTakenBy [a ?playerRole] }
            UNION
            {tic-tac-toe:Square13 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square23 tic-tac-toe:moveTakenBy [a ?playerRole] .
            tic-tac-toe:Square33 tic-tac-toe:moveTakenBy [a ?playerRole] }
                        
            ?winner a ?playerRole.        
        } 
        """)
                    
        for row in a:
            return row['winner']
        
        return None
    

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
        if square_url in free_squares:
            return True
        
        return False
    

    def get_board(self):
        free_squares = self.get_free_squares()
        occupied_squares = self.get_occupied_squares()
        board = {}
        
        for a in free_squares:
            board[a] = ""

        for b in occupied_squares:
            board[b] = occupied_squares[b]

        return board
    

    def get_occupied_squares(self):
        a = self.graph.query("""
        SELECT ?s ?p
        WHERE {
            ?s tic-tac-toe:moveTakenBy ?p
        }
        """)

        squares = {}         
        for row in a:
            print(row)
            squares[row['s']]=row['p']
        
        return squares
    


    def get_free_squares(self):
        a = self.graph.query("""
        SELECT ?s
        WHERE {
            ?s rdf:type owl:Class .
            ?s rdfs:subClassOf tic-tac-toe:Square
            FILTER NOT EXISTS { ?s tic-tac-toe:moveTakenBy ?p }
        }
        """)

        squares = []         
        for row in a:
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
            print("X Player Role: " + s)
        
        print("*board:*")
        # Get the squares
        row1, row2, row3 = self.get_board_visual() 
        print(row1)
        print(row2)
        print(row3)

    
    def get_board_visual(self):
        row1 = ""   
        row1 = self.get_square_desc(self.ttt.Square11, row1)
        row1 = self.get_square_desc(self.ttt.Square12, row1)
        row1 = self.get_square_desc(self.ttt.Square13, row1)
        row2 = ""   
        row2 = self.get_square_desc(self.ttt.Square21, row2)
        row2 = self.get_square_desc(self.ttt.Square22, row2)
        row2 = self.get_square_desc(self.ttt.Square23, row2)
        row3 = ""   
        row3 = self.get_square_desc(self.ttt.Square31, row3)
        row3 = self.get_square_desc(self.ttt.Square32, row3)
        row3 = self.get_square_desc(self.ttt.Square33, row3)
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