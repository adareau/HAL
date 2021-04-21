# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1348, 797)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(840, 550, 89, 25))
        self.testButton.setObjectName("testButton")
        self.dayBrowserBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dayBrowserBox.setGeometry(QtCore.QRect(10, 10, 161, 291))
        self.dayBrowserBox.setObjectName("dayBrowserBox")
        self.dayList = QtWidgets.QListWidget(self.dayBrowserBox)
        self.dayList.setGeometry(QtCore.QRect(120, 70, 31, 211))
        self.dayList.setObjectName("dayList")
        self.monthList = QtWidgets.QListWidget(self.dayBrowserBox)
        self.monthList.setGeometry(QtCore.QRect(80, 70, 31, 211))
        self.monthList.setObjectName("monthList")
        self.yearList = QtWidgets.QListWidget(self.dayBrowserBox)
        self.yearList.setGeometry(QtCore.QRect(10, 70, 61, 211))
        self.yearList.setObjectName("yearList")
        self.dateEdit = QtWidgets.QDateEdit(self.dayBrowserBox)
        self.dateEdit.setGeometry(QtCore.QRect(10, 30, 141, 24))
        self.dateEdit.setObjectName("dateEdit")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 310, 311, 361))
        self.groupBox.setObjectName("groupBox")
        self.seqList = QtWidgets.QListWidget(self.groupBox)
        self.seqList.setGeometry(QtCore.QRect(160, 30, 141, 321))
        self.seqList.setObjectName("seqList")
        self.runList = QtWidgets.QListWidget(self.groupBox)
        self.runList.setGeometry(QtCore.QRect(10, 30, 141, 321))
        self.runList.setObjectName("runList")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1348, 20))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "HAL"))
        self.testButton.setText(_translate("mainWindow", "Test"))
        self.dayBrowserBox.setTitle(_translate("mainWindow", "Day browser"))
        self.groupBox.setTitle(_translate("mainWindow", "Run browser"))
