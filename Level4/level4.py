# this AI will improve upon level 3 by utilising alpha and beta pruning


import chess
import time


class AiEngine:
    def __init__(self, depth):
        self.chessBoard = chess.Board()
        self.colour = chess.BLACK
        self.depth = depth

    def oppositionMove(self, opposition):
        # apply the oppositionsa move to the Ai model of the chess board
        self.chessBoard.push_uci(opposition)

    def getMove(self):
        tic = time.perf_counter()
        bestMove, _, totalMovesEvaluated = self.__get_move_alphaBeta(self.chessBoard, 0, -float("inf"), float("inf"))
        toc = time.perf_counter()
        # apply the selected move to own model of chess board
        self.chessBoard.push(bestMove)
        print("I have evaluated ", totalMovesEvaluated, " moves, it took ", (toc - tic), "s, to a depth of ", self.depth)
        return bestMove.uci()

    def __get_move_alphaBeta(self, board, depth, alpha, beta):
        # Terminal node, return value of node
        if depth == self.depth:
            return board.peek(), self.__evaluate_board(board), 1
        else:
            if board.turn == self.colour:  # my turn, maximise the score
                highestScore = -1000
                bestMove = None
                totalMovesEvaluated = 0
                for move in board.legal_moves:
                    board.push(move)
                    _, localScore, movesEvaluated = self.__get_move_alphaBeta(board, depth + 1, alpha, beta)
                    totalMovesEvaluated += movesEvaluated
                    if localScore > highestScore:
                        bestMove = move
                        highestScore = localScore
                    alpha = max(alpha, localScore)
                    board.pop()
                    if alpha >= beta:
                        break
                return bestMove, highestScore, totalMovesEvaluated
            else:  # opponent turn, minimise the score
                lowestScore = 1000
                bestMove = None
                totalMovesEvaluated = 0
                for move in board.legal_moves:
                    board.push(move)
                    _, localScore, movesEvaluated = self.__get_move_alphaBeta(board, depth + 1, alpha, beta)
                    totalMovesEvaluated += movesEvaluated
                    if localScore < lowestScore:
                        bestMove = move
                        lowestScore = localScore
                    beta = min(beta, localScore)
                    board.pop()
                    if alpha >= beta:
                        break
                return bestMove, lowestScore, totalMovesEvaluated
        raise Exception("You should not have gotten here, alpha beta get move")
        

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

        if chessPiece.color != self.colour:  # check if it is our piece or opponent piece
            value = value * -1

        return value
