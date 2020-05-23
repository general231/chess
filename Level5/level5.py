# This will improve on level 4 with a more advancded evaluation function
from math import floor

import chess
import time


class AiEngine:
    def __init__(self, depth):
        self.chessBoard = chess.Board()
        self.colour = chess.BLACK
        self.depth = depth

    def oppositionMove(self, opposition):
        # apply the opposition's move to the Ai model of the chess board
        self.chessBoard.push_uci(opposition)

    def getMove(self):
        tic = time.perf_counter()
        best_move, _, total_moves_evaluated = self.__get_move_alphaBeta(self.chessBoard, 0, -float("inf"), float("inf"))
        toc = time.perf_counter()
        # apply the selected move to own model of chess board
        self.chessBoard.push(best_move)
        print("I have evaluated ", total_moves_evaluated, " moves, it took ", (toc - tic), "s, to a depth of ",
              self.depth)
        return best_move.uci()

    def __get_move_alphaBeta(self, board, depth, alpha, beta):
        # Terminal node, return value of node
        if depth == self.depth:
            return board.peek(), self.__evaluate_board(board), 1
        else:
            if board.turn == self.colour:  # my turn, maximise the score
                highest_score = -1000
                best_move = None
                total_moves_evaluated = 0
                for move in board.legal_moves:
                    board.push(move)
                    _, local_score, moves_evaluated = self.__get_move_alphaBeta(board, depth + 1, alpha, beta)
                    total_moves_evaluated += moves_evaluated
                    if local_score > highest_score:
                        best_move = move
                        highest_score = local_score
                    alpha = max(alpha, local_score)
                    board.pop()
                    if alpha >= beta:
                        break
                return best_move, highest_score, total_moves_evaluated
            else:  # opponent turn, minimise the score
                lowest_score = 1000
                best_move = None
                total_moves_evaluated = 0
                for move in board.legal_moves:
                    board.push(move)
                    _, local_score, moves_evaluated = self.__get_move_alphaBeta(board, depth + 1, alpha, beta)
                    total_moves_evaluated += moves_evaluated
                    if local_score < lowest_score:
                        best_move = move
                        lowest_score = local_score
                    beta = min(beta, local_score)
                    board.pop()
                    if alpha >= beta:
                        break
                return best_move, lowest_score, total_moves_evaluated
        raise Exception("You should not have gotten here, alpha beta get move")

    def __evaluate_board(self, chess_board):
        # this function evaluates the value of pieces on the board and returns
        # check for end game
        if chess_board.is_checkmate():
            if chess_board.turn:
                return -9999
            else:
                return 9999
        if chess_board.is_stalemate():
            return 0
        if chess_board.is_insufficient_material():
            return 0

        current_board_value = 0
        for square, chessPiece in self.chessBoard.piece_map().items():
            piece_value = self.__get_piece_value(chessPiece)
            position_value = self.__get_piece_position_value(chessPiece, square)
            total_value = piece_value + position_value
            total_value = total_value if chessPiece.color == self.colour else total_value*-1
            current_board_value += total_value

        return current_board_value

    def __get_piece_value(self, chess_piece):
        # pawns are worth 1 point, bishops and knights are worth 3 points, rooks 5 points, queen 8 points and king 9000
        # Reinfield values
        if chess_piece.piece_type == chess.PAWN:
            value = 1
        elif chess_piece.piece_type == chess.KNIGHT:
            value = 3
        elif chess_piece.piece_type == chess.BISHOP:
            value = 3
        elif chess_piece.piece_type == chess.ROOK:
            value = 5
        elif chess_piece.piece_type == chess.QUEEN:
            value = 9
        elif chess_piece.piece_type == chess.KING:
            value = 9000
        else:
            raise Exception("Invalid chess piece type: ", chess_piece)

        return value

    def __get_piece_position_value(self, chessPiece, square):
        row = square % 8
        column = floor(square / 8)
        if chessPiece.color == chess.BLACK:
            column = 7 - column
        if chessPiece.piece_type == chess.PAWN:
            position_table = self.__get_pawn_position_table()
        elif chessPiece.piece_type == chess.KNIGHT:
            position_table = self.__get_knight_position_table()
        elif chessPiece.piece_type == chess.BISHOP:
            position_table = self.__get_bishop_position_table()
        elif chessPiece.piece_type == chess.ROOK:
            position_table = self.__get_rook_position_table()
        elif chessPiece.piece_type == chess.QUEEN:
            position_table = self.__get_queen_position_table()
        elif chessPiece.piece_type == chess.KING:
            position_table = self.__get_king_midgame_position_table()
        else:
            raise Exception("Invalid chess piece type: ", chessPiece)

        return position_table[column][row]

    # piece square values taken from https://www.chessprogramming.org/Simplified_Evaluation_Function#Piece-Square_Tables
    # changed to work with the points range above
    def __get_pawn_position_table(self):
        # this is the position values for white, flip for black
        return [[0, 0, 0, 0, 0, 0, 0, 0],
                [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
                [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
                [0.0, 0.0, 0.0, 0.2, 0.2, 0, 0, 0],
                [0.05, -0.05, -0.1, 0, 0, -0.1, -0.05, -0.05],
                [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
                [0, 0, 0, 0, 0, 0, 0, 0]
                ]
    def __get_knight_position_table(self):
        # these are the position values for a white knight, flip for black
        return [[-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
                [-0.4, -0.2, 0, 0, 0, 0, -0.2, -0.4],
                [-0.3, 0, 0.1, 0.15, 0.15, 0.1, 0, -0.3],
                [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
                [-0.3, 0, 0.15, 0.2, 0.2, 0.15, 0, -0.3],
                [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
                [-0.4, -0.2, 0, 0.05, 0.05, 0, -0.2, -0.4],
                [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
                ]
    def __get_bishop_position_table(self):
        return [[-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
                [-0.1, 0, 0, 0, 0, 0, 0, -0.1],
                [-0.1, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.1],
                [-0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, -0.1],
                [-0.1, 0, 0.1, 0.1, 0.1, 0.1, 0, -0.1],
                [-0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1],
                [-0.1, 0.05, 0, 0, 0, 0, 0.05, -0.1],
                [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
                ]
    def __get_rook_position_table(self):
        return [[0, 0, 0, 0, 0, 0, 0, 0],
                [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05],
                [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
                [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
                [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
                [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
                [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
                [0, 0, 0, 0.05, 0.05, 0, 0, 0]
                ]
    def __get_queen_position_table(self):
        return [[-0.2, -0.1, -0.1, -5, -5, -0.1, -0.1, -0.2],
                [-0.1, 0, 0, 0, 0, 0, 0, -0.1],
                [-0.1, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.1],
                [-0.05, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.05],
                [0, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.05],
                [-0.1, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.1],
                [-0.1, 0, 0.05, 0, 0, 0, 0, -0.1],
                [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]
                ]
    def __get_king_midgame_position_table(self):
        return [[-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
                [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
                [0.2, 0.2, 0, 0, 0, 0, 0.2, 0.2],
                [0.2, 0.3, 0.1, 0, 0, 0.1, 0.3, 0.2]
                ]
