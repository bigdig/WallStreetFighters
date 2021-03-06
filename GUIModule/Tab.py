# -*- coding: utf-8 -*-
import sys
from qtpy import QtGui,QtCore,QtWidgets
from Calendar import Calendar

def tabUi(self,showLists=True):
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        """Każdą zakładkę dzielimy jak na razie na 3 obszary: opcje,
        listy , wykresy """
        
        """Ramka przechowujaca listy"""
        if showLists:
                self.listsFrame = QtWidgets.QFrame(self)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.listsFrame.sizePolicy().hasHeightForWidth())
                self.listsFrame.setSizePolicy(sizePolicy)
                # ustawimy maksymalna szerokosc kolumny na 350
                self.listsFrame.setMaximumSize(QtCore.QSize(600, 16777215))
                self.listsFrame.setMinimumSize(QtCore.QSize(550, 0))
                self.listsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.listsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.listsFrame.setLineWidth(3)
        

                #ustawiamy zarządce rozkładu vertical
                self.listsLayout = QtWidgets.QVBoxLayout(self.listsFrame)
                # textline
                self.filterLineEdit = QtWidgets.QLineEdit(self.listsFrame)
                self.listsLayout.addWidget(self.filterLineEdit)
                # Tool Box przechowujący listy
                self.listsToolBox = QtWidgets.QToolBox(self.listsFrame)

                #Index
                self.indexPage = QtWidgets.QWidget(self.listsFrame)
                self.indexPageLayout = QtWidgets.QHBoxLayout(self.indexPage)
                self.listsToolBox.addItem(self.indexPage, "Index")
                self.indexListView = QtWidgets.QTableView(self.listsFrame)
                self.indexListView.setAlternatingRowColors(True)
                self.indexListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                self.indexListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                tableStyle(self,self.indexListView) #ustawiamy styl tabeli
                self.indexPageLayout.addWidget(self.indexListView)

                #Stock
                self.stockPage = QtWidgets.QWidget(self.listsFrame)
                self.stockPageLayout = QtWidgets.QGridLayout(self.stockPage)
                self.stockPageLayout.setSpacing(0)
                self.listsToolBox.addItem(self.stockPage , "Stock")

                self.nasdaqButton = QtWidgets.QPushButton("NASDAQ",self.listsFrame)
                self.nasdaqButton.setCheckable(True)
                self.nasdaqButton.setAutoExclusive(True)
                self.stockPageLayout.addWidget(self.nasdaqButton, 0, 0, 1, 1)
                self.nyseButton = QtWidgets.QPushButton("NYSE",self.listsFrame)
                self.nyseButton.setCheckable(True)
                self.nyseButton.setAutoExclusive(True)
                self.stockPageLayout.addWidget(self.nyseButton, 0, 1, 1, 1)
                self.amexButton = QtWidgets.QPushButton("AMEX",self.listsFrame)
                self.amexButton.setCheckable(True)
                self.amexButton.setAutoExclusive(True)
                self.stockPageLayout.addWidget(self.amexButton, 1, 0, 1, 1)
                self.wigButton = QtWidgets.QPushButton("WIG",self.listsFrame)
                self.wigButton.setCheckable(True)
                self.wigButton.setAutoExclusive(True)
                self.stockPageLayout.addWidget(self.wigButton, 1, 1, 1, 1)
                self.wig20Button = QtWidgets.QPushButton("WIG20",self.listsFrame)
                self.wig20Button.setCheckable(True)
                self.wig20Button.setAutoExclusive(True)
                self.stockPageLayout.addWidget(self.wig20Button, 0, 2, 1, 1)
                self.allButton = QtWidgets.QPushButton("ALL",self.listsFrame)
                self.allButton.setCheckable(True)
                self.allButton.setChecked(True)
                self.allButton.setAutoExclusive(True)
                self.stockPageLayout.addWidget(self.allButton, 1, 2, 1, 1)
               
                self.stockListView = QtWidgets.QTableView(self.listsFrame)
                self.stockListView.setAlternatingRowColors(True)
                self.stockListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                #self.stockListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                tableStyle(self,self.stockListView)#ustawiamy styl tabeli
                self.stockPageLayout.addWidget(self.stockListView,2,0,1,3)

                #forex
                self.forexPage = QtWidgets.QWidget(self.listsFrame)
                self.forexPageLayout = QtWidgets.QHBoxLayout(self.forexPage)
                self.listsToolBox.addItem(self.forexPage, "Forex")
                self.forexListView = QtWidgets.QTableView(self.listsFrame)
                self.forexListView.setAlternatingRowColors(True)
                self.forexListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                #self.forexListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                tableStyle(self,self.forexListView)#ustawiamy styl tabeli
                self.forexPageLayout.addWidget(self.forexListView)

                #Bond
                self.bondPage = QtWidgets.QWidget(self.listsFrame)
                self.bondPageLayout = QtWidgets.QHBoxLayout(self.bondPage)
                self.listsToolBox.addItem(self.bondPage, "Bond")
                self.bondListView = QtWidgets.QTableView(self.listsFrame)
                self.bondListView.setAlternatingRowColors(True)
                self.bondListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                #self.bondListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                tableStyle(self,self.bondListView)
                self.bondPageLayout.addWidget(self.bondListView)

                #Resource
                self.resourcePage = QtWidgets.QWidget(self.listsFrame)
                self.resourcePageLayout = QtWidgets.QHBoxLayout(self.resourcePage)
                self.listsToolBox.addItem(self.resourcePage, "Resource")
                self.resourceListView = QtWidgets.QTableView(self.listsFrame)
                self.resourceListView.setAlternatingRowColors(True)
                self.resourceListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                #self.resourceListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                tableStyle(self,self.resourceListView)
                self.resourcePageLayout.addWidget(self.resourceListView)


                #Futures contract
                self.futuresContractPage = QtWidgets.QWidget(self.listsFrame)
                self.futuresContractPageLayout = QtWidgets.QHBoxLayout(self.futuresContractPage)
                self.listsToolBox.addItem(self.futuresContractPage, "Futures Contract")
                self.futuresListView = QtWidgets.QTableView(self.listsFrame)
                self.futuresListView.setAlternatingRowColors(True)
                self.futuresListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                #self.futuresListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                tableStyle(self,self.futuresListView)
                self.futuresContractPageLayout.addWidget(self.futuresListView)
        
                self.listsLayout.addWidget(self.listsToolBox)
                # koniec Tool Box

                #compare
                self.compareWidget = QtWidgets.QWidget(self.listsFrame)
                self.compareLayout = QtWidgets.QHBoxLayout(self.compareWidget)
                self.compareCheckBox = QtWidgets.QCheckBox("Enable Compare",self.listsFrame)
                self.compareLayout.addWidget(self.compareCheckBox)
                self.compareLineEdit = QtWidgets.QLineEdit(self.listsFrame)
                self.compareLineEdit.setEnabled(False)
                self.compareLineEdit.setToolTip("e.g. ^DJI vs FLWS vs ...")
                self.compareLayout.addWidget(self.compareLineEdit)
                self.compareButton = QtWidgets.QPushButton("Compare",self.listsFrame)
                self.compareButton.setEnabled(False)
                self.compareButton.setToolTip("Click to Compare")
                self.compareLayout.addWidget(self.compareButton)
                self.listsLayout.addWidget(self.compareWidget)

                self.horizontalLayout.addWidget(self.listsFrame)
        # koniec ramki przechowywyjącej listy
        

        """Ramka przechowujaca opcjie i wykres"""
        self.optionsAndChartsFrame = QtWidgets.QFrame(self)
        # ustawimy maksymalna szerokosc kolumny na 350
        #self.optionsAndChartsFrame.setMaximumSize(QtCore.QSize(1600, 16777215))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.optionsAndChartsFrame.sizePolicy().hasHeightForWidth())
        self.optionsAndChartsFrame.setSizePolicy(sizePolicy)
        self.optionsAndChartsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.optionsAndChartsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.optionsAndChartsFrame)

        """Ramka przechowujaca wykresy"""
        self.chartsFrame = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.chartsFrame.sizePolicy().hasHeightForWidth())
        self.chartsFrame.setSizePolicy(sizePolicy)
        self.chartsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chartsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chartsFrame.setLineWidth(3)
        #ustawiamy zarządce rozkładu vertical
        self.chartsLayout = QtWidgets.QVBoxLayout(self.chartsFrame)
        self.verticalLayout.addWidget(self.chartsFrame)

        """Ramka przechowujaca opcje"""
        self.optionsFrame = QtWidgets.QFrame(self)
        # ustawimy maksymalna wysokosc na 120

        self.optionsFrame.setMaximumSize(QtCore.QSize(16777215, 150))
        self.optionsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.optionsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.optionsFrame.setLineWidth(3)
        #ustawiamy zarządce rozkładu Grid
        self.optionsLayout = QtWidgets.QGridLayout(self.optionsFrame)
        
        #pola do wprowadzania okresu
        self.label = QtWidgets.QLabel('Range:',self.optionsFrame) 
        self.optionsLayout.addWidget(self.label,0,0,1,1)
        self.startDateEdit = QtWidgets.QDateEdit(self.optionsFrame)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setCalendarWidget(Calendar())
        self.startDateEdit.setDate(QtCore.QDate.currentDate().addDays(-30))
        self.startDateEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(1))
        self.optionsLayout.addWidget(self.startDateEdit,1,0,1,1)
        self.endDateEdit = QtWidgets.QDateEdit(self.optionsFrame)
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarWidget(Calendar())
        self.endDateEdit.setDate(QtCore.QDate.currentDate().addDays(-30))
        self.endDateEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(1))
        self.optionsLayout.addWidget(self.endDateEdit,2,0,1,1)
        self.dateButton = QtWidgets.QPushButton('Ok',self.optionsFrame)
        self.optionsLayout.addWidget(self.dateButton,3,0,1,1)
        #koniec pola do wprowadzania okresu
	self.verticalLayout.addWidget(self.optionsFrame)
        
        #dodajemy ramke zawierajaca wykres i opcje do tab
        self.horizontalLayout.addWidget(self.optionsAndChartsFrame)

        

def addChartButton(self):
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(6)

        # Step combo box
        self.stepLabel = QtWidgets.QLabel('Step',self.optionsFrame)#label Step
        self.gridLayout.addWidget(self.stepLabel,0,0,1,1)
        self.stepComboBox = QtWidgets.QComboBox(self.optionsFrame)
        self.stepComboBox.addItem('daily')
        self.stepComboBox.addItem('weekly')
        self.stepComboBox.addItem('monthly')
        self.gridLayout.addWidget(self.stepComboBox,1,0,1,1)
        # show chart Patterns
        self.showChartPatternsButton = QtWidgets.QPushButton('Show chart patterns',self.optionsFrame)
        self.gridLayout.addWidget(self.showChartPatternsButton,2,0,1,2)
        # chartType comboBox
        self.chartTypeLabel = QtWidgets.QLabel('Chart Type',self.optionsFrame)#label Chart Type
        self.gridLayout.addWidget(self.chartTypeLabel,0,1,1,1)
        self.chartTypeComboBox = QtWidgets.QComboBox(self.optionsFrame)
        self.chartTypeComboBox.addItem('line')
        self.chartTypeComboBox.addItem('point')
        self.chartTypeComboBox.addItem('candlestick')
        self.chartTypeComboBox.addItem('bar')
        self.gridLayout.addWidget(self.chartTypeComboBox,1,1,1,1)
        # Scale Type
        self.scaleTypeLabel = QtWidgets.QLabel('Scale',self.optionsFrame)
        self.gridLayout.addWidget(self.scaleTypeLabel,0,2,1,1)
        self.linearRadioButton = QtWidgets.QRadioButton('linear',self.optionsFrame)
        self.gridLayout.addWidget(self.linearRadioButton,1,2,1,1)
        self.linearRadioButton.setChecked(True)
        self.logRadioButton = QtWidgets.QRadioButton('log',self.optionsFrame)
        self.gridLayout.addWidget(self.logRadioButton,2,2,1,1)
        #wyłaczenie voluminu
        self.volumenCheckBox = QtWidgets.QCheckBox('Hide Volumen',self.optionsFrame)
        self.gridLayout.addWidget(self.volumenCheckBox,0,3,1,1)
        #wlacznie możliwości rysowania na wykeresie
        self.paintCheckBox = QtWidgets.QCheckBox('Enable painting',self.optionsFrame)
        self.gridLayout.addWidget(self.paintCheckBox,1,3,1,1)
        #przycisk do analizy
        self.analyzeButton = QtWidgets.QPushButton('Analyze',self.optionsFrame)
        self.gridLayout.addWidget(self.analyzeButton,2,3,1,1)
	#Spacer
        #self.spacer = QtGui.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, 		QtWidgets.QSizePolicy.Expanding)
        #self.gridLayout.addItem(self.spacer,0,5,1,3)
        return self.frame

def tableStyle(self,table):
        # hide grid
        table.setShowGrid(False)
        # set the font
        font = QtGui.QFont("Courier New", 10)
        table.setFont(font)
        # hide vertical header
        vh = table.verticalHeader()
        vh.setVisible(False)
        # set column width to fit contents
        table.resizeColumnsToContents()
        # set horizontal header properties
        hh = table.horizontalHeader()
        hh.setStretchLastSection(True)
        
        # enable sorting
        table.setSortingEnabled(True)


        

        
                
        
        
         
    
