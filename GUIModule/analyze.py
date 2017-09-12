# -*- coding: utf-8 -*-
from qtpy import QtWidgets, QtGui, QtCore
import DataParserModule.dataParser as dataParser
import time

class Analyze (QtWidgets.QWidget):
        def __init__(self):
                QtWidgets.QWidget.__init__(self)
                self.initUi()
        def initUi(self):
                self.layout = QtWidgets.QHBoxLayout(self)
                self.textBrowser = QtWidgets.QTextBrowser(self)
                self.layout.addWidget(self.textBrowser)
