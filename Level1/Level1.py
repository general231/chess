# First attempt to get a chess playing program, this is mostly to make sure the computer can play chess and the backend
# chess stuff works before it becomes intelligent

import random
import chess


class AiEngine:
    def __init__(self):
        self.chessBoard = chess.Board()

    def oppositionMove(self, opposition):
        self.chessBoard.push_uci(opposition)

    def getMove(self):
        highestScore = -1000
        bestMove = None
        for move in self.chessBoard.legal_moves:
            testBoard = self.chessBoard
            # Apply the move
            testBoard.push(move)
            # check how the move affects the board
            move_score = self.__evaluate_board(testBoard)
            # If it is the best scrore so far save it
            if move_score > highestScore:
                highestScore = move_score
                bestMove = move
            # undo the move so you can test the next chess move
            testBoard.pop()
        # apply the selected move to own model of chess board
        self.chessBoard.push(bestMove)

        return bestMove.uci()

    def __evaluate_board(self, chessBoard):
        # this function evaluates the value of pieces on the board and returns
        # check for end game
        if chessBoard.is_checkmate():
            if chessBoard.turn:
                return -9999
            else:
                return 9999
        if chessBoard.is_stalemate():
            return 0
        if chessBoard.is_insufficient_material():
            return 0

        # score the board with a random number for level 1
        eval = 1000*random.random()

        return eval

    def printBoard(self):
        print(self.chessBoard)

