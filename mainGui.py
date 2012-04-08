# -*- coding: utf-8 -*-

import sys
import datetime
import operator

import os
from PyQt4 import QtGui, QtCore
from TabA import TabA
import cPickle
import GUIModule.RSSgui as RSSgui
from ChartsModule.Chart import Chart
import DataParserModule.dataParser as dataParser

class GuiMainWindow(object):
    """Klasa odpowiedzialna za GUI głownego okna aplikacji"""
    def setupGui(self,MainWindow):
        """ustawianie komponetów GUI"""
        MainWindow.setObjectName("WallStreetFighters")
        MainWindow.resize(1000,700)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        #tabs - przechowywanie zakładek
	self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.tabs = QtGui.QTabWidget(self.centralWidget)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 980, 640))
        self.tabs.setObjectName("Tabs")
        self.tabs.setTabsClosable(True)

        #załadowanie List
        os.chdir("../WallStreetFighters/DataParserModule")
        dataParser.loadData()

        # inicjujemy model danych dla Index
        self.indexModel = self.ListModel(list=dataParser.INDEX_LIST)
        # inicjujemy model danych dla Stock
        self.stockModel = self.ListModel(list=dataParser.STOCK_LIST)
        # inicjujemy model danych dla Forex
        self.forexModel = self.ListModel(list=dataParser.FOREX_LIST)
        # inicjujemy model danych dla Resources
        self.resourceModel = self.ListModel(list=dataParser.RESOURCE_LIST)
        # inicjujemy model danych dla Bond
        self.bondModel = self.ListModel(list=dataParser.BOND_LIST)
        



        """tab A wskaźniki i oscylatory"""
	self.tabA = TabA(self.indexModel,self.stockModel,self.forexModel,self.bondModel,self.resourceModel,)
        self.tabs.addTab(self.tabA,"tabA")
        
        self.tabA.indexListView.doubleClicked.connect(self.newIndexTab)
        self.tabA.stockListView.doubleClicked.connect(self.newStockTab)
        self.tabA.forexListView.doubleClicked.connect(self.newForexTab)
        self.tabA.bondListView.doubleClicked.connect(self.newBondTab)
        self.tabA.resourceListView.doubleClicked.connect(self.newResourceTab)
        self.rssWidget = RSSgui.RSSWidget(self.tabA)
        self.tabA.chartsLayout.addWidget(self.rssWidget)
        self.tabA.compareButton.clicked.connect(self.compare)

        
        """koniec tab A """
        
        """ tab B
        self.tabB = AbstractTab()
        self.tabB.setObjectName("tabB")

        #przycisk wyswietlanie wykresu (przyciski dodajemy na sam koniec okna)
        self.tabB.optionsLayout.addWidget(self.tabB.addChartButton(),0,4,3,4)
        self.tabs.addTab(self.tabB,"tabB")
        koniec tab B"""

        """ tabC
        self.tabC = AbstractTab()
        self.tabC.setObjectName("tabC")
        self.tabs.addTab(self.tabC,"tabC")
        self.tabC.optionsLayout.addWidget(self.tabC.addChartButton(),0,7,3,4)
        self.tabs.addTab(self.tabC,"tabC")
        
        Koniec tabC"""
        
    
	""" koniec ustawiania Zakładek"""

	self.tabs.tabCloseRequested.connect(self.closeTab)
	
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralWidget)

				
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)        
        
    def compare(self):
        pageIndex = self.tabA.listsToolBox.currentIndex()
        if pageIndex == 0:
            qModelIndex = self.tabA.indexListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newIndexTab(qModelIndex,"Indices' comparison")
        if pageIndex == 1:
            qModelIndex = self.tabA.stockListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newStockTab(qModelIndex,"Stocks' comparison")
        if pageIndex == 2:
            qModelIndex = self.tabA.forexListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newForexTab(qModelIndex,"Forex comparison")
        if pageIndex == 3:
            qModelIndex = self.tabA.bondListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newBondTab(qModelIndex,"Bonds' comparison")
        if pageIndex == 4:
            qModelIndex = self.tabA.resourceListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newResourceTab(qModelIndex,"Resources' comparison")
        
    #metody otwierajace nowe zakladki po podwójnym kliknięciu
    def newIndexTab(self,qModelIndex,nameTab = None):
        self.tabA1 = TabA(qModelIndex = qModelIndex,settings = self.settings(),listName = "index",showLists = False)
        if not nameTab:
            nameTab = self.tabA.indexListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def newStockTab(self,qModelIndex,nameTab = None):
        self.tabA1 = TabA(qModelIndex = qModelIndex,settings = self.settings(),listName = "stock",showLists = False)
        if not nameTab:
            nameTab = self.tabA.stockListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))
    def newForexTab(self,qModelIndex,nameTab = None):
        self.tabA1 = TabA(qModelIndex = qModelIndex,settings = self.settings(),listName = "forex",showLists = False)
        if not nameTab:
            nameTab = self.tabA.forexListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def newBondTab(self,qModelIndex,nameTab = None):
        self.tabA1 = TabA(qModelIndex = qModelIndex,settings = self.settings(),listName = "bond",showLists = False)
        if not nameTab:
            nameTab = self.tabA.bondListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def newResourceTab(self,qModelIndex,nameTab = None):
        self.tabA1 = TabA(qModelIndex = qModelIndex,settings = self.settings(),listName = "resource",showLists = False)
        if not nameTab:
            nameTab = self.tabA.resourceListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def settings(self):
        #funkcja pobiera aktualnie zaznaczone opcje z tabA
        dateStart = self.tabA.startDateEdit.date()  # początek daty
        start = datetime.datetime(dateStart.year(),dateStart.month(),dateStart.day())
        
        dateEnd = self.tabA.endDateEdit.date()     # koniec daty
        end = datetime.datetime(dateEnd.year(),dateEnd.month(),dateEnd.day())
        indicator = []
        if self.tabA.smaCheckBox.isChecked():
            indicator.append("SMA")
        if self.tabA.wmaCheckBox.isChecked():
            indicator.append("WMA")
        if self.tabA.emaCheckBox.isChecked():
            indicator.append("EMA")
        if self.tabA.bollingerCheckBox.isChecked():
            indicator.append("bollinger")
        oscilator = ''
        if self.tabA.momentumCheckBox.isChecked():
            oscilator = "momentum"
        elif self.tabA.cciCheckBox.isChecked():
            oscilator = "CCI"
        elif self.tabA.rocCheckBox.isChecked():
            oscilator = "ROC"
        elif self.tabA.rsiCheckBox.isChecked():
            oscilator = "RSI"
        elif self.tabA.williamsCheckBox.isChecked():
            oscilator = "williams"
        #step
        step = self.tabA.stepComboBox.currentText()
        #scale
        if self.tabA.logRadioButton.isChecked():
            scale = 'log'
        else:
            scale = 'linear'
        #chartType
        chartType = self.tabA.chartTypeComboBox.currentText()
        hideVolumen =self.tabA.volumenCheckBox.isChecked() 
        #painting
        painting = self.tabA.paintCheckBox.isChecked() 
        t = {"start":start,"end":end,"indicator":indicator,"step":step,
             "chartType":chartType,"hideVolumen":hideVolumen,
             "painting":painting,"scale":scale,"oscilator":oscilator}
        return t
    def closeTab(self,i):
        if i != 0:
            self.tabs.removeTab(i)
            
    """ Modele przechowywania listy dla poszczególnych instrumentów finansowych"""
    class ListModel(QtCore.QAbstractTableModel):
        def __init__(self,list, parent = None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self.list = list
            k = 0 
            for li in list:
                li.append(k)
                k+=1
            self.headerdata = ['symbol', 'name', '']
        def mainIndex(self):
            return 3

        
        def rowCount(self, parent):
            return len(self.list)
        def columnCount(self,parent):
            return 2
        def headerData(self, col, orientation, role):
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self.headerdata[col])
            return QtCore.QVariant()
        
        def data(self, index, role):
            if not index.isValid():
                return QtCore.QVariant()
            elif role == QtCore.Qt.WhatsThisRole:
                return self.list[index.row()]
            elif role != QtCore.Qt.DisplayRole:
                return QtCore.QVariant()
            if index.column() == 2:
                return QtCore.QVariant(self.list[index.row()][index.column()+2])
            else:
                return QtCore.QVariant(self.list[index.row()][index.column()])
        
        def sort(self, Ncol, order):
            """Sort table by given column number.
            """
            self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
            self.list = sorted(self.list, key=operator.itemgetter(Ncol))        
            if order == QtCore.Qt.DescendingOrder:
                self.list.reverse()
            self.emit(QtCore.SIGNAL("layoutChanged()"))
