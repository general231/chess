# An improvement on level 1, this AI will try and evaluate the board using a points based system for each piece, still a bad AI but it should take pieces if presented with the opportunity

import chess

class AiEngine:
    def __init__(self):
        self.chessBoard = chess.Board()
        self.colour = chess.BLACK

    def oppositionMove(self, opposition):
        # apply the oppositions move to the Ai model of the chess board
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

        eval = 0;
        for chessPiece in self.chessBoard.piece_map().values():
            eval += self.__get_piece_value(chessPiece)

        return eval

    def __get_piece_value(self, chessPiece):
        # pawns are worth 1 point, bishops and knights are worth 3 points, rooks 5 points, queen 8 points and king 9000
        # AI pieces are positive, opponents pieces are negative
        if chessPiece.piece_type == chess.PAWN:
            value = 1
        elif chessPiece.piece_type == chess.KNIGHT:
            value = 3
        elif chessPiece.piece_type == chess.BISHOP:
            value = 3
        elif chessPiece.piece_type == chess.ROOK:
            value = 5
        elif chessPiece.piece_type == chess.QUEEN:
            value = 8
        elif chessPiece.piece_type == chess.KING:
            value = 9000
        else:
            raise Exception("Invalid chess piece type: ", chessPiece)

        if chessPiece.color != self.colour: # check if it is our piece or opponent piece
            value = value * -1

        return value