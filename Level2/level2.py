# An improvement on level 1, this AI will try and evaluate the board using a points based system for each piece

import chess

class AiEngine:
    def __init__(self):
        self.chessBoard = chess.Board()
        self.colour = chess.Color.BLACK

    def oppositionMove(self, opposition):
        # apply the oppositions move to the Ai model of the chess board
        self.chessBoard.push_uci(opposition)

    def getMove(self):
        # Calculate the optimal move for the chess ai
        return 1

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
        # pawns are worth 1 point, bishops and knights are worth 3 points, rooks 5 points, queen 8 points and king 9000
        # AI pieces are positive, oponent pieces are negative
        

        return eval
