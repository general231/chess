# This AI will improve on level 2 by using a search tree with min max
import time

import chess

class AiEngine:
    def __init__(self, depth):
        self.chessBoard = chess.Board()
        self.colour = chess.BLACK
        self.depth = depth

    def oppositionMove(self, opposition):
        # apply the oppositionsa move to the Ai model of the chess board
        self.chessBoard.push_uci(opposition)

    def getMove(self):
        highest_score = -1000
        bestMove = None
        totalMovesEvaluated = 0
        tic = time.perf_counter()
        for move in self.chessBoard.legal_moves:
            testBoard = self.chessBoard
            # Apply the move
            testBoard.push(move)
            # check how the move affects the board
            _, move_score, moves_evaluated = self.__get_move_minmax(testBoard, 0)
            totalMovesEvaluated += moves_evaluated
            # If it is the best scrore so far save it
            if move_score > highest_score:
                highest_score = move_score
                bestMove = move
            # undo the move so you can test the next chess move
            testBoard.pop()
        toc = time.perf_counter()
        # apply the selected move to own model of chess board
        self.chessBoard.push(bestMove)
        print("I have evaluated ", totalMovesEvaluated, " moves, it took ", (toc-tic), "s, to a depth of 1")
        return bestMove.uci()

    def __get_move_minmax(self, board, depth):
        # end condition, don't go any further
        if depth == self.depth:
            if board.turn == self.colour:
                highestScore = -1000
                bestMove = None
                movesEvaluated = 0
                for move in board.legal_moves:
                    movesEvaluated += 1
                    board.push(move)
                    localScore = self.__evaluate_board(board)
                    if localScore > highestScore:
                        bestMove = move
                        highestScore = localScore
                    board.pop()
                return bestMove, highestScore, movesEvaluated
            else:
                lowestScore = 1000
                bestMove = None
                movesEvaluated = 0
                for move in board.legal_moves:
                    movesEvaluated += 1
                    board.push(move)
                    localScore = self.__evaluate_board(board)
                    if localScore < lowestScore:
                        bestMove = move
                        lowestScore = localScore
                    board.pop()
                return bestMove, lowestScore, movesEvaluated


        else:
            if board.turn == self.colour: # my turn, maximise the score
                highestScore = -1000
                bestMove = None
                totalMovesEvaluated = 0
                for move in board.legal_moves:
                    board.push(move)
                    _, localScore, movesEvaluated = self.__get_move_minmax(board, depth+1)
                    totalMovesEvaluated += movesEvaluated
                    if localScore > highestScore:
                        bestMove = move
                        highestScore = localScore
                    board.pop()
                return bestMove, highestScore, totalMovesEvaluated
            else: # opponent turn, minimise the score
                lowestScore = 1000
                bestMove = None
                totalMovesEvaluated = 0
                for move in board.legal_moves:
                    board.push(move)
                    _, localScore, movesEvaluated = self.__get_move_minmax(board, depth+1) # end condition should always go off AI turn
                    totalMovesEvaluated += movesEvaluated
                    if localScore < lowestScore:
                        bestMove = move
                        lowestScore = localScore
                    board.pop()
                return bestMove, lowestScore, totalMovesEvaluated

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