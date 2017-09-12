import sys
from qtpy import QtGui,QtCore,QtWidgets
def Calendar():
        cal = QtWidgets.QCalendarWidget()
        cal.setGridVisible(True)
        cal.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        cal.setFirstDayOfWeek(QtCore.Qt.Monday)
        cal.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        return cal
