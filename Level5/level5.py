# This will improve on level 4 with a more advancded evaluation function


import chess

class AiEngine:
    def __init__(self):
        self.chessBoard = chess.Board()

    def oppositionMove(self, opposition):
        # apply the oppositionsa move to the Ai model of the chess board
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
        eval = 1

        return eval