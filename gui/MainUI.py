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
        mainWindow.resize(958, 648)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(330, 100, 89, 25))
        self.testButton.setObjectName("testButton")
        self.yearListView = QtWidgets.QListView(self.centralwidget)
        self.yearListView.setGeometry(QtCore.QRect(20, 60, 61, 211))
        self.yearListView.setObjectName("yearListView")
        self.monthListView = QtWidgets.QListView(self.centralwidget)
        self.monthListView.setGeometry(QtCore.QRect(90, 60, 31, 211))
        self.monthListView.setObjectName("monthListView")
        self.dayListView = QtWidgets.QListView(self.centralwidget)
        self.dayListView.setGeometry(QtCore.QRect(130, 60, 31, 211))
        self.dayListView.setObjectName("dayListView")
        self.fileList = QtWidgets.QListWidget(self.centralwidget)
        self.fileList.setGeometry(QtCore.QRect(20, 280, 141, 321))
        self.fileList.setObjectName("fileList")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(20, 20, 141, 24))
        self.dateEdit.setObjectName("dateEdit")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 958, 20))
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
