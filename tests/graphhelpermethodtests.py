import unittest
from rdflib import Graph, URIRef, Namespace, RDF, Literal
from rdflib.namespace import NamespaceManager

from graphhelpermethods import GraphHelperMethods

class TestGraphMethods(unittest.TestCase):

    apiBot = URIRef("http://localhost:8083/apibot")
    agentZero = URIRef("http://localhost:7070/agentzero")
    tttgame = URIRef("http://localhost:8083/game/id=1")
    
    def setUp(self):
        
        # Setup 
        g = Graph()
        g.parse('TicTacToe.owl')
        self.helper = GraphHelperMethods(g,'tic-tac-toe',self.tttgame, self.apiBot, self.agentZero, Literal("someId"))


    # Tests
    def test_get_square_url_for_int(self):
        #No first move
        #Test getting it from the graph
        result = self.helper.get_square_url_for_int(12)
        self.assertEqual( self.helper.ttt.Square12, result)
        result = self.helper.get_square_url_for_int(11)
        self.assertEqual( self.helper.ttt.Square11, result)
        result = self.helper.get_square_url_for_int(13)
        self.assertEqual( self.helper.ttt.Square13, result)
        result = self.helper.get_square_url_for_int(21)
        self.assertEqual( self.helper.ttt.Square21, result)
        result = self.helper.get_square_url_for_int(22)
        self.assertEqual( self.helper.ttt.Square22, result)
        result = self.helper.get_square_url_for_int(23)
        self.assertEqual( self.helper.ttt.Square23, result)
        result = self.helper.get_square_url_for_int(31)
        self.assertEqual( self.helper.ttt.Square31, result)
        result = self.helper.get_square_url_for_int(32)
        self.assertEqual( self.helper.ttt.Square32, result)
        result = self.helper.get_square_url_for_int(33)
        self.assertEqual( self.helper.ttt.Square33, result)


    # Tests
    def test_get_first_move_when_none_made(self):
        #No first move
        #Test getting it from the graph
        result = self.helper.get_first_move()

        self.assertEqual(None, result)


    def test_add_and_get_first_move(self):
        #Expected first move
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        #Test getting it from the graph
        result = self.helper.get_first_move()

        self.assertEqual(self.helper.ttt.Square13, result)
        #The graph should have one move with the property 'self.tic_tac_toe_namespace.firstMove', and it should be square13
        for s, p, o in self.helper.graph.triples((self.helper.game, self.helper.ttt.firstMove, None)):
            # Should only be one
            self.assertEqual(self.helper.ttt.Square13, o)


    def test_add_and_get_next_move(self):
        #Expected first move
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        #Next add this
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        result = self.helper.get_next_move(self.helper.ttt.Square13)

        self.assertEqual(self.helper.ttt.Square11, result)

        #Check this is also the last move
        result = self.helper.get_last_move()
        self.assertEqual(self.helper.ttt.Square11, result)
        #The graph should have one move with the property 'self.tic_tac_toe_namespace.nexttMove', and it should be square 11
        for s, p, o in self.helper.graph.triples((self.helper.game, self.helper.ttt.nextMove, None)):
            # Should only be one
            self.assertEqual(self.helper.ttt.Square11, o)


    def test_get_board_all_empty(self):
        squares = self.helper.get_board()
        #There are 9 squares in the board
        self.assertEqual(9, len(squares))
        #None of them have a move in them
        for v in squares.values():
            self.assertEqual(0, len(v))


    def test_get_board_some_occupied(self):
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        squares = self.helper.get_board()
        print("test_get_board_some_occupied squares:")
        for s in squares:
            print(s, squares[s])
            
        count = 0
        #There are 9 squares in the board
        self.assertEqual(9, len(squares))
        for v in squares.values():
            if (len(v) > 0):
                count = count + 1

        #Two of them have a move in them
        self.assertEqual(2, count)

    def test_check_winner_diagonal_right_left(self):
        # O O X
        # - X -
        # X - -
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square31, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_diagonal_left_right(self):
        # X O O
        # - X -
        # - - X
        self.helper.add_move(self.helper.ttt.Square11, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square13, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_row_1(self):
        # X X X
        # O O -
        # - - -
        self.helper.add_move(self.helper.ttt.Square11, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square21, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square12, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square22, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_row_2(self):
        # O O -
        # X X X
        # - - -
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square23, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_row_3(self):
        # O O -
        # - - -
        # X X X
        self.helper.add_move(self.helper.ttt.Square31, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square32, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_col_1(self):
        # X O -
        # X O -
        # X - -
        self.helper.add_move(self.helper.ttt.Square11, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square22, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square31, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_col_2(self):
        # O X O
        # - X -
        # - X -
        self.helper.add_move(self.helper.ttt.Square12, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square13, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square32, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_col_3(self):
        # O O X 
        # - - X
        # - - X
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square23, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        
        self.assertEqual(self.apiBot, self.helper.get_winner())


    def test_check_winner_o_player(self):
        # O O O 
        # - X X
        # - - X
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square23, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square13, self.agentZero)
        
        self.assertEqual(self.agentZero, self.helper.get_winner())

    
    def test_check_winner_o_player_different_ordered_moves(self):
        # O O O 
        # - X X
        # - - X
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square13, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square23, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square12, self.agentZero)
        
        self.assertEqual(self.agentZero, self.helper.get_winner())


    def test_check_winner_draw(self):
        # O O X 
        # X X O
        # O O X
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square31, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square23, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square32, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square12, self.apiBot)
        
        self.assertEqual(None, self.helper.get_winner())


    def test_check_free_squares(self):
        # No moves yet, should get all squares
        squares = self.helper.get_free_squares()
        #All squares should be free
        print(len(squares))
        self.assertEqual(len(squares), 9)
        self.assertIn(self.helper.ttt.Square11, squares)
        self.assertIn(self.helper.ttt.Square12, squares)
        self.assertIn(self.helper.ttt.Square13, squares)
        self.assertIn(self.helper.ttt.Square21, squares)
        self.assertIn(self.helper.ttt.Square22, squares)
        self.assertIn(self.helper.ttt.Square23, squares)
        self.assertIn(self.helper.ttt.Square31, squares)
        self.assertIn(self.helper.ttt.Square32, squares)
        self.assertIn(self.helper.ttt.Square33, squares)
        
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        
        # Should get all squares except 13 and 11
        squares = self.helper.get_free_squares()
        self.assertIn(self.helper.ttt.Square12, squares)
        self.assertIn(self.helper.ttt.Square21, squares)
        self.assertIn(self.helper.ttt.Square22, squares)
        self.assertIn(self.helper.ttt.Square23, squares)
        self.assertIn(self.helper.ttt.Square31, squares)
        self.assertIn(self.helper.ttt.Square32, squares)
        self.assertIn(self.helper.ttt.Square33, squares)
        self.assertNotIn(self.helper.ttt.Square13, squares)
        self.assertNotIn(self.helper.ttt.Square11, squares)
        self.assertEqual(len(squares), 7)

        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square31, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square23, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        
        #Now should only be 2 left
        squares = self.helper.get_free_squares()
        self.assertEqual(len(squares), 2)
        self.assertIn(self.helper.ttt.Square32, squares)
        self.assertIn(self.helper.ttt.Square12, squares)
        self.assertNotIn(self.helper.ttt.Square11, squares)
        self.assertNotIn(self.helper.ttt.Square13, squares)
        self.assertNotIn(self.helper.ttt.Square21, squares)
        self.assertNotIn(self.helper.ttt.Square22, squares)
        self.assertNotIn(self.helper.ttt.Square23, squares)
        self.assertNotIn(self.helper.ttt.Square31, squares)
        self.assertNotIn(self.helper.ttt.Square33, squares)

        self.helper.add_move(self.helper.ttt.Square12, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square32, self.agentZero)

        # Now none left
        squares = self.helper.get_free_squares()
        self.assertEqual(len(squares), 0)


    def test_print_game(self):
        print("******* PRINTING GAME *******")
        self.helper.print_game();

        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square31, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square23, self.agentZero)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        
        print("******* PRINTING GAME *******")  
        self.helper.print_game();


    def test_is_game_over_draw(self):
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square31, self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square23, self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(self.helper.ttt.Square33, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square11, self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(self.helper.ttt.Square12, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square32, self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(self.helper.ttt.Square13, self.apiBot)
        self.assertEqual(self.helper.is_game_over(), True)


    def test_is_game_over_win(self):
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square31, self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square33, self.agentZero)
        self.assertEqual(self.helper.is_game_over(), False)
        self.helper.add_move(self.helper.ttt.Square23, self.apiBot)
        self.assertEqual(self.helper.is_game_over(), True)


    def test_is_square_free(self):
        # True if game still in play
        self.assertEqual(self.helper.is_square_free(self.helper.ttt.Square21), True)
        self.helper.add_move(self.helper.ttt.Square21, self.apiBot)
        # False if square taken
        self.assertEqual(self.helper.is_square_free(self.helper.ttt.Square21), False)
        # True if game still in play 
        self.assertEqual(self.helper.is_square_free(self.helper.ttt.Square11), True)
        # False if game is over
        self.helper.add_move(self.helper.ttt.Square22, self.apiBot)
        self.helper.add_move(self.helper.ttt.Square23, self.apiBot)
        self.assertEqual(self.helper.is_square_free(self.helper.ttt.Square11), False)