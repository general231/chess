import Level1.Level1
import ChessEngine.gui
import PyQt5.QtWidgets
import sys

level = 4

if level == 1:
    from Level1.Level1 import AiEngine
    depth = 0
elif level == 2:
    from Level2.level2 import AiEngine
    depth = 0
elif level == 3:
    from Level3.level3 import AiEngine
    depth = 4
elif level == 4:
    from Level4.level4 import AiEngine
    depth = 6
elif level == 5:
    from Level5.Level5 import AiEngine



aiEngine = AiEngine(depth)

app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = ChessEngine.gui.ChessScreen(aiEngine)
sys.exit(app.exec_())