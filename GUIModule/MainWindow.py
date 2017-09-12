import sys
from qtpy import QtGui
from mainGui import GuiMainWindow

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        # obiekt Gui
        self.gui = GuiMainWindow()
        self.gui.setupGui(self)


    
    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    
