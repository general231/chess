import sys
from math import floor

import PyQt5.QtWidgets
import PyQt5.QtSvg
import PyQt5.QtGui

import chess
import chess.svg


class ChessScreen(PyQt5.QtWidgets.QWidget):

    def __init__(self, aiEngine):
        super().__init__()

        if aiEngine == None:
            raise Exception("Ai engine must be passed into the gui")
        self.chessBoard = chess.Board()
        self.aiEngine = aiEngine
        self.__init_UI()

    def __init_UI(self):
        self.moveLabel = PyQt5.QtWidgets.QLabel()
        self.moveLabel.setText("Legal Moves:")

        self.moveLineEdit = PyQt5.QtWidgets.QLineEdit()
        self.moveLineEdit.resize(50, 15)
        self.moveButton = PyQt5.QtWidgets.QPushButton("Go")
        self.moveButton.clicked.connect(self.move_list_clicked)
        self.moveHbox = PyQt5.QtWidgets.QHBoxLayout()
        self.moveHbox.addWidget(self.moveLineEdit)
        self.moveHbox.addWidget(self.moveButton)

        self.moveList = PyQt5.QtWidgets.QListView()
        self.listModel = PyQt5.QtGui.QStandardItemModel()
        self.moveList.setModel(self.listModel)
        self.__update_move_list()
        
        self.moveVbox = PyQt5.QtWidgets.QVBoxLayout()
        self.moveVbox.addLayout(self.moveHbox)
        self.moveVbox.addWidget(self.moveList)
        #self.moveList.clicked.connect(self.move_list_clicked)

        self.historyTextEdit = PyQt5.QtWidgets.QTextEdit()

        self.chessBoardDisplay = PyQt5.QtSvg.QSvgWidget()
        self.chessBoardDisplay.setGeometry(0, 0, 400, 400)  # origin at 0, 0 in a 400x400 pixel image
        svg_bytes = bytearray(chess.svg.board(board=self.chessBoard, size=400), encoding='utf-8')
        self.chessBoardDisplay.renderer().load(svg_bytes)

        self.grid = PyQt5.QtWidgets.QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.chessBoardDisplay, 0, 0)
        self.grid.addLayout(self.moveVbox, 0, 1)
        self.grid.addWidget(self.historyTextEdit, 1, 0)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle("Chess")

        self.show()

    def move_list_clicked(self):
        uciMove = self.moveLineEdit.text().lower()
        if not self.__uci_is_legal_move(uciMove):
            self.moveLineEdit.setStyleSheet("color: red")
            return None
        self.moveLineEdit.clear()
        #uciMove = self.moveLineEdit.setText("")
        self.chessBoard.push_uci(uciMove)

        # let the AI move
        self.aiEngine.oppositionMove(uciMove)
        aiMove = self.aiEngine.getMove()
        self.chessBoard.push_uci(aiMove)

        self.__update_move_list()
        self.__update_chessBoardDisplay()
        # check for endgame
        self.__check_for_endgame()

    def __update_move_list(self):
        #self.moveList.clear()
        legal_moves = self.chessBoard.legal_moves
        for moveIdx in range(0, legal_moves.count()):
            item = PyQt5.QtGui.QStandardItem(self.__move_to_words(self.chessBoard, list(legal_moves)[moveIdx]))
            self.listModel.appendRow(item)

    def __move_to_words(self, board, move):
        start_square = move.from_square
        starting_square_string = self.__chessSquareToCoordinate(start_square)
        end_square = move.to_square
        end_square_string = self.__chessSquareToCoordinate(end_square)
        chess_piece = board.piece_map()[start_square]
        chess_piece_name = chess.piece_name(chess_piece.piece_type)
        chess_piece_colour = "White" if chess_piece.color else "Black"

        return chess_piece_colour + " " + chess_piece_name + " move from " + starting_square_string + " to " + end_square_string

    def __chessSquareToCoordinate(self, square):
        row = square % 8
        column = floor(square / 8) + 1
        stringName = str(chr(ord('A') + row)) + str(column)
        return stringName

    def __update_chessBoardDisplay(self):
        svg_bytes = bytearray(chess.svg.board(board=self.chessBoard, size=400), encoding='utf-8')
        self.chessBoardDisplay.renderer().load(svg_bytes)
        self.chessBoardDisplay.update()

    def __check_for_endgame(self):
        if self.chessBoard.is_game_over():
            print("Game over")
            sys.exit()

    def __uci_is_legal_move(self, strMoveUci):
        for move in self.chessBoard.legal_moves:
            if move.uci() == strMoveUci:
                return True
        return False
