from graphhelpermethods import GraphHelperMethods

class APIBOT():

    def __init__(self, uri, helper):
        self.uri = uri
        self.helper = helper
    

    def make_move(self):
        free_squares = self.helper.get_free_squares()
        if (len(free_squares) > 0):
            self.helper.add_move(free_squares[0], self.uri)
            return True
        else:
            return False