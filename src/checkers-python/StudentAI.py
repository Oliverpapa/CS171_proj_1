from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy

# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
# Group name: ArtificialStupidity2
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


def getProtected(coord, other):
    possible_coord = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
    for o in other:
        if [coord[0] - o[0], coord[1] - o[1]] in possible_coord:
            return True
    return False


def abPruning(copySelf, depth, Max, Min, player):
    moves = flatMoves(copySelf.board.get_all_possible_moves(player))
    if depth == 0:
        result = moves[0]
        for move in moves:
            copySelf.board.make_move(move, copySelf.color)
            max, min = abPruning(copySelf, depth + 1, Max, Min, 3 - copySelf.color)
            copySelf.board.undo()
            if min > Max:
                Max = min
                result = move
        return result
    elif depth == copySelf.depth:
        if player == copySelf.color:
            for move in moves:
                score = copySelf.heuristic_func(move, copySelf.color)
                if score > Max:
                    Max = score
                if Max >= Min:
                    break
            return Max, Min
        else:
            for move in moves:
                score = copySelf.heuristic_func(move, 3 - copySelf.color)
                if score < Min:
                    Min = score
                if Max >= Min:
                    break
            return Max, Min
    else:
        for move in moves:
            if player == copySelf.board.is_win(colorDictInv[copySelf.color]) == copySelf.color:
                return math.inf, Min
            elif player == copySelf.board.is_win(colorDictInv[3 - copySelf.color]) == 3 - copySelf.color:
                return Max, -math.inf
            copySelf.board.make_move(move, player)
            max, min = abPruning(copySelf, depth + 1, Max, Min, 3 - player)
            copySelf.board.undo()
            if player == copySelf.color:
                if min > Max:
                    Max = min
                if Max >= Min:
                    break
            else:
                if max < Min:
                    Min = max
                if Max >= Min:
                    break
        return Max, Min


# def simple_search(copySelf):
#     moves1 = flatMoves(copySelf.board.get_all_possible_moves(copySelf.color))
#     Max1 = -math.inf
#     Min1 = math.inf
#     move = moves1[0]
#     for move1 in moves1:
#         copySelf.board.make_move(move1, copySelf.color)
#         if copySelf.board.is_win(colorDictInv[copySelf.color]) == copySelf.color:
#             return move1
#         moves2 = flatMoves(copySelf.board.get_all_possible_moves(3 - copySelf.color))
#         for move2 in moves2:
#             Max2 = copy.copy(Max1)
#             Min2 = copy.copy(Min1)
#             copySelf.board.make_move(move2, 3 - copySelf.color)
#             if copySelf.board.is_win(colorDictInv[3 - copySelf.color]) == 3 - copySelf.color:
#                 Min2 = -math.inf
#             moves3 = flatMoves(copySelf.board.get_all_possible_moves(copySelf.color))
#             for move3 in moves3:
#                 Max3 = copy.copy(Max2)
#                 Min3 = copy.copy(Min2)
#                 score = copySelf.heuristic_func(move3, copySelf.color)
#                 if score > Max3:
#                     Max3 = score
#                 if Max3 >= Min3:
#                     break
#             copySelf.board.undo()
#             if Max3 < Min2:
#                 Min2 = Max3
#             if Max2 >= Min2:
#                 break
#         copySelf.board.undo()
#         if Min2 > Max1:
#             Max1 = Min2
#             move = move1
#     return move


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
        self.depth = 4
        self.a = -math.inf
        self.b = math.inf

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
        # print(move)
        self.board.make_move(move, self.color)
        return move

    def select_move(self, moves):
        """take a list of moves and select the best one,
        return move"""
        copySelf = copy.deepcopy(self)

        return abPruning(copySelf, 0, self.a, self.b, self.color)
        # return simple_search(copySelf)

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
        black = []
        white = []
        for row in self.board.board:
            for checker in row:
                if colorDict[checker.get_color()] == 1:
                    black.append(checker.get_location())
                else:
                    white.append(checker.get_location())
        # for row in self.board.board:
        #     for checker in row:
        #         add = 1 if colorDict[checker.get_color()] == self.color else -1
        #         y = checker.get_location()[1]
        #         if self.color == 1:
        #             # if getProtected(checker.get_location(), black) and add == 1:
        #             #     result += 5
        #             if checker.is_king:
        #                 result += (self.board.row + 1 + y) * add
        #             else:
        #                 result += (y + 5) * add
        #         else:
        #             # if getProtected(checker.get_location(), white) and add == 1:
        #             #     result += 5
        #             if checker.is_king:
        #                 result += (self.board.row + 1) * add
        #             else:
        #                 result += (4 + self.board.row - y) * add
        for row in self.board.board:
            for checker in row:
                y = checker.get_location()[1]
                x = checker.get_location()[0]
                if colorDict[checker.get_color()] == self.color:
                    if self.color == 2 and y == self.board.row - 1:
                        result += 0.5
                    elif self.color == 1 and y == 0:
                        result += 0.5
                    if x == 0 or x == self.board.col - 1:
                        result += 0.25
                    if checker.is_king:
                        result += 3.0 + 0.5*abs(y-(self.board.row/2.0))
                    else:
                        result += 1.5
                else:
                    if checker.is_king:
                        result -= 3.0
                    else:
                        result -= 1.5

        self.board.undo()
        return result


