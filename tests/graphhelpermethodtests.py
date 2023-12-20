import unittest
from rdflib import Graph, URIRef, Namespace, RDF, Literal
from rdflib.namespace import NamespaceManager

from graphhelpermethods import GraphHelperMethods

class TestGraphMethods(unittest.TestCase):

    apiBot = URIRef("http://localhost:8083/apibot")
    agentZero = URIRef("http://localhost:7070/agentzero")
    
    def setUp(self):
        
        # Setup 
        g = Graph()
        g.parse('TicTacToe.owl')
        self.helper = GraphHelperMethods(g,'tic-tac-toe',"http://localhost:8083/",self.apiBot, self.agentZero, Literal("someId"))


    # Tests
    def test_get_first_move_when_none_made(self):
        #No first move
        #Test getting it from the graph
        result = self.helper.get_first_move()

        self.assertEqual(None, result)


    def test_add_and_get_first_move(self):
        #Expected first move
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        #Test getting it from the graph
        result = self.helper.get_first_move()

        self.assertEqual(URIRef("http://localhost:8083/Square13?id=someId"), result)
        #The graph should have one move with the property 'self.tic_tac_toe_namespace.firstMove', and it should be square13
        for s, p, o in self.helper.graph.triples((self.helper.game, self.helper.ttt.firstMove, None)):
            # Should only be one
            self.assertEqual(URIRef("http://localhost:8083/Square13?id=someId"), o)


    def test_add_and_get_next_move(self):
        #Expected first move

        sq13 = URIRef("http://localhost:8083/Square13?id=someId")
        self.helper.add_move(sq13, self.apiBot)
        #Next add this
        sq11 = URIRef("http://localhost:8083/Square11?id=someId")
        self.helper.add_move(sq11, self.agentZero)
        result = self.helper.get_next_move(sq13)

        self.assertEqual(sq11, result)

        #Check this is also the last move
        result = self.helper.get_last_move()
        self.assertEqual(sq11, result)
        #The graph should have one move with the property 'self.tic_tac_toe_namespace.nexttMove', and it should be square 11
        for s, p, o in self.helper.graph.triples((self.helper.game, self.helper.ttt.nextMove, None)):
            # Should only be one
            self.assertEqual(sq11, o)


    def test_get_board_occupied_all_empty(self):
        squares = self.helper.get_board_occupied()
        #There are 9 squares in the board, none of them have a move in them
        self.assertEqual(0, len(squares))
        


    def test_get_board_some_occupied(self):
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        squares = self.helper.get_board_occupied()
        print("test_get_board_some_occupied squares:")
        for s in squares:
            print(s, squares[s])
            
        count = 0
        #There are 9 squares in the board but only two are occupied
        self.assertEqual(2, len(squares))


    def test_square_to_square_instance(self):
        expected_square_instance = URIRef("http://localhost:8083/Square11?id=someId")

        result = self.helper.square_to_square_instance(self.helper.ttt.Square11)
        self.assertEqual(expected_square_instance, result)


    def test_square_instance_to_square(self):
        square_instance = URIRef("http://localhost:8083/Square11?id=someId")

        result = self.helper.square_instance_to_square(square_instance)
        self.assertEqual(self.helper.ttt.Square11, result)


    def test_get_winner_diagonal_right_left(self):
        # O O X
        # - X -
        # X - -
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.apiBot)
        winner = self.helper.get_winner()
        print(winner)
        self.assertEqual(self.apiBot, winner)




    def test_get_winner_diagonal_left_right(self):
        # X O O
        # - X -
        # - - X
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_row_1(self):
        # X X X
        # O O -
        # - - -
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_row_2(self):
        # O O -
        # X X X
        # - - -
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_row_3(self):
        # O O -
        # - - -
        # X X X
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square32?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_col_1(self):
        # X O -
        # X O -
        # X - -
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_col_2(self):
        # O X O
        # - X -
        # - X -
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square32?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_col_3(self):
        # O O X 
        # - - X
        # - - X
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_get_winner_o_player(self):
        # O O O 
        # - X X
        # - - X
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.agentZero)
        
        self.assertEqual(self.agentZero, self.helper.get_winner())

    
    def test_get_winner_o_player_different_ordered_moves(self):
        # O O O 
        # - X X
        # - - X
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.agentZero)
        
        self.assertEqual(self.agentZero, self.helper.get_winner())


    def test_get_winner_draw(self):
        # O O X 
        # X X O
        # O O X
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square32?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.apiBot)
        
        self.assertEqual(None, self.helper.get_winner())


    def test_check_free_squares(self):
        # No moves yet, should get all squares
        squares = self.helper.get_free_squares()
        #All squares should be free
        print(len(squares))
        self.assertEqual(len(squares), 9)
        sq11 = URIRef("http://localhost:8083/Square11?id=someId")
        sq12 = URIRef("http://localhost:8083/Square12?id=someId")
        sq13 = URIRef("http://localhost:8083/Square13?id=someId")
        sq21 = URIRef("http://localhost:8083/Square21?id=someId")
        sq22 = URIRef("http://localhost:8083/Square22?id=someId")
        sq23 = URIRef("http://localhost:8083/Square23?id=someId")
        sq31 = URIRef("http://localhost:8083/Square31?id=someId")
        sq32 = URIRef("http://localhost:8083/Square32?id=someId")
        sq33 = URIRef("http://localhost:8083/Square33?id=someId")

        self.assertIn(sq11, squares)
        self.assertIn(sq12, squares)
        self.assertIn(sq13, squares)
        self.assertIn(sq21, squares)
        self.assertIn(sq22, squares)
        self.assertIn(sq23, squares)
        self.assertIn(sq31, squares)
        self.assertIn(sq32, squares)
        self.assertIn(sq33, squares)
        
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        
        # Should get all squares except 13 and 11
        squares = self.helper.get_free_squares()

        self.assertNotIn(sq11, squares)
        self.assertIn(sq12, squares)
        self.assertNotIn(sq13, squares)
        self.assertIn(sq21, squares)
        self.assertIn(sq22, squares)
        self.assertIn(sq23, squares)
        self.assertIn(sq31, squares)
        self.assertIn(sq32, squares)
        self.assertIn(sq33, squares)

        self.assertEqual(len(squares), 7)

        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        
        #Now should only be 2 left
        squares = self.helper.get_free_squares()
        self.assertEqual(len(squares), 2)

        self.assertNotIn(sq11, squares)
        self.assertIn(sq12, squares)
        self.assertNotIn(sq13, squares)
        self.assertNotIn(sq21, squares)
        self.assertNotIn(sq22, squares)
        self.assertNotIn(sq23, squares)
        self.assertNotIn(sq31, squares)
        self.assertIn(sq32, squares)
        self.assertNotIn(sq33, squares)

        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square32?id=someId"), self.agentZero)

        # Now none left
        squares = self.helper.get_free_squares()
        self.assertEqual(len(squares), 0)


    def test_print_game(self):
        print("******* PRINTING GAME *******")
        self.helper.print_game();

        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.agentZero)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        
        print("******* PRINTING GAME *******")  
        self.helper.print_game();


    def test_is_game_over_draw(self):
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square11?id=someId"), self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(URIRef("http://localhost:8083/Square12?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square32?id=someId"), self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(URIRef("http://localhost:8083/Square13?id=someId"), self.apiBot)
        self.assertEqual(self.helper.is_game_over(), True)


    def test_is_game_over_win(self):
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square31?id=someId"), self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square33?id=someId"), self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.apiBot)
        self.assertEqual(self.helper.is_game_over(), True)


    def test_is_square_free(self):
        # True if game still in play
        value = self.helper.is_square_free(URIRef("http://localhost:8083/Square21?id=someId"));
        self.assertEqual(value, True)
        self.helper.add_move(URIRef("http://localhost:8083/Square21?id=someId"), self.apiBot)
        # False if square taken
        self.assertEqual(self.helper.is_square_free(URIRef("http://localhost:8083/Square21?id=someId")), False)
        # True if game still in play 
        self.assertEqual(self.helper.is_square_free(URIRef("http://localhost:8083/Square11?id=someId")), True)
        # False if game is over
        self.helper.add_move(URIRef("http://localhost:8083/Square22?id=someId"), self.apiBot)
        self.helper.add_move(URIRef("http://localhost:8083/Square23?id=someId"), self.apiBot)
        self.assertEqual(self.helper.is_square_free(URIRef("http://localhost:8083/Square11?id=someId")), False)