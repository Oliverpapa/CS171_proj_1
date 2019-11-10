from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy

# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.

colorDict = {
    "B": 1,
    "W": 2,
    ".": -1
}

colorDictInv = {
    1: "B",
    2: "W",
    -1: "."
}


def flatMoves(m):
    result = []
    for c in m:
        for move in c:
            result.append(move)
    return result


def abPruning(copySelf, depth):
    pass


def simple_search(copySelf):
    moves1 = flatMoves(copySelf.board.get_all_possible_moves(copySelf.color))
    Max1 = -math.inf
    Min1 = math.inf
    move = moves1[0]
    for move1 in moves1:
        copySelf.board.make_move(move1, copySelf.color)
        if copySelf.board.is_win(colorDictInv[copySelf.color]) == copySelf.color:
            return move1
        moves2 = flatMoves(copySelf.board.get_all_possible_moves(3 - copySelf.color))
        for move2 in moves2:
            Max2 = copy.copy(Max1)
            Min2 = copy.copy(Min1)
            copySelf.board.make_move(move2, 3 - copySelf.color)
            if copySelf.board.is_win(colorDictInv[3 - copySelf.color]) == 3 - copySelf.color:
                Min2 = -math.inf
            moves3 = flatMoves(copySelf.board.get_all_possible_moves(copySelf.color))
            for move3 in moves3:
                Max3 = copy.copy(Max2)
                Min3 = copy.copy(Min2)
                score = copySelf.heuristic_func(move3, copySelf.color)
                if score > Max3:
                    Max3 = score
                if Max3 >= Min3:
                    break
            copySelf.board.undo()
            if Max3 < Min2:
                Min2 = Max3
            if Max2 >= Min2:
                break
        copySelf.board.undo()
        if Min2 > Max1:
            Max1 = Min2
            move = move1
    return move


class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.depth = 2
        self.a = 0
        self.b = 0

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        # index = randint(0, len(moves) - 1)
        # inner_index = randint(0, len(moves[index]) - 1)
        # move = moves[index][inner_index]
        move = self.select_move(moves)
        self.board.make_move(move, self.color)
        return move

    def select_move(self, moves):
        """take a list of moves and select the best one,
        return move"""
        copySelf = copy.deepcopy(self)
        self.a = -math.inf
        self.b = math.inf

        return simple_search(copySelf)

    def heuristic_func(self, move, color):
        """take a move, evaluate it's heuristic value
        return the value"""
        result = 0
        colorDict = {
            "B": 1,
            "W": 2,
            ".": 0
        }
        self.board.make_move(move, color)
        # print (self.board.board)
        for row in self.board.board:
            for checker in row:
                if colorDict[checker.get_color()] == self.color:
                    y = checker.get_location()[1]
                    if self.color == 1:
                        result += y + 5
                    else:
                        result += 4 + self.board.row - y
                elif checker.is_king:
                    result += 2
        self.board.undo()
        return result
