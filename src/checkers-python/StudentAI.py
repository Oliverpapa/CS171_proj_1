from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        # index = randint(0, len(moves) - 1)
        # inner_index = randint(0, len(moves[index]) - 1)
        # move = moves[index][inner_index]
        move = self.select_move(moves)
        self.board.make_move(move,self.color)
        return move

    def select_move(self,moves):
        """take a list of moves and select the best one,
        return move"""
        best = [0, -99]     # store the best move in a list with its heuristic value
        for checker in moves:
            for move in checker:
                if self.heuristic_func(move) > best[1]:
                    best[0] = move
                    best[1] = self.heuristic_func(move)
        print (type(best[0]))
        return best[0]


    def heuristic_func(self, move):
        """take a move, evaluate it's heuristic value
        return the value"""
        result = 0
        self.board.make_move(move,self.color)
        print (self.board.board)
        for row in self.board.board:
            for checker in row:
                if checker.get_color == self.color:
                    x = checker.get_location()[0]
                    y = checker.get_location()[1]
                    result += y
        self.board.undo()
        return result

