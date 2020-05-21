import Level1.Level1
import ChessEngine.gui
import PyQt5.QtWidgets
import sys

level = 1

if level == 1:
    from Level1.Level1 import AiEngine
elif level == 2:
    from Level2.Level2 import AiEngine
elif level == 3:
    from Level3.Level3 import AiEngine
elif level == 4:
    from Level4.Level4 import AiEngine
elif level == 5:
    from Level5.Level5 import AiEngine



aiEngine = AiEngine()

app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = ChessEngine.gui.ChessScreen(aiEngine)
sys.exit(app.exec_())