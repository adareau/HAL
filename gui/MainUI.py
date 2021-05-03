# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1465, 903)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dayBrowserBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dayBrowserBox.setGeometry(QtCore.QRect(10, 10, 161, 321))
        self.dayBrowserBox.setObjectName("dayBrowserBox")
        self.dayList = QtWidgets.QListWidget(self.dayBrowserBox)
        self.dayList.setGeometry(QtCore.QRect(120, 70, 31, 241))
        self.dayList.setObjectName("dayList")
        self.monthList = QtWidgets.QListWidget(self.dayBrowserBox)
        self.monthList.setGeometry(QtCore.QRect(80, 70, 31, 241))
        self.monthList.setObjectName("monthList")
        self.yearList = QtWidgets.QListWidget(self.dayBrowserBox)
        self.yearList.setGeometry(QtCore.QRect(10, 70, 61, 241))
        self.yearList.setObjectName("yearList")
        self.dateEdit = QtWidgets.QDateEdit(self.dayBrowserBox)
        self.dateEdit.setGeometry(QtCore.QRect(10, 30, 101, 24))
        self.dateEdit.setObjectName("dateEdit")
        self.todayButton = QtWidgets.QPushButton(self.dayBrowserBox)
        self.todayButton.setGeometry(QtCore.QRect(120, 30, 31, 24))
        self.todayButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/today.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.todayButton.setIcon(icon)
        self.todayButton.setIconSize(QtCore.QSize(24, 24))
        self.todayButton.setObjectName("todayButton")
        self.runBrowserBox = QtWidgets.QGroupBox(self.centralwidget)
        self.runBrowserBox.setGeometry(QtCore.QRect(10, 340, 461, 391))
        self.runBrowserBox.setObjectName("runBrowserBox")
        self.seqList = QtWidgets.QListWidget(self.runBrowserBox)
        self.seqList.setGeometry(QtCore.QRect(160, 50, 141, 301))
        self.seqList.setObjectName("seqList")
        self.runList = QtWidgets.QListWidget(self.runBrowserBox)
        self.runList.setGeometry(QtCore.QRect(10, 50, 141, 301))
        self.runList.setObjectName("runList")
        self.setList = QtWidgets.QListWidget(self.runBrowserBox)
        self.setList.setGeometry(QtCore.QRect(310, 50, 141, 301))
        self.setList.setObjectName("setList")
        self.label_4 = QtWidgets.QLabel(self.runBrowserBox)
        self.label_4.setGeometry(QtCore.QRect(13, 30, 57, 15))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.runBrowserBox)
        self.label_5.setGeometry(QtCore.QRect(160, 30, 71, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.runBrowserBox)
        self.label_6.setGeometry(QtCore.QRect(312, 30, 51, 16))
        self.label_6.setObjectName("label_6")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.runBrowserBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 357, 291, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.refreshRunListButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.refreshRunListButton.setObjectName("refreshRunListButton")
        self.horizontalLayout_3.addWidget(self.refreshRunListButton)
        self.fitButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.fitButton.setObjectName("fitButton")
        self.horizontalLayout_3.addWidget(self.fitButton)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.runBrowserBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(309, 357, 254, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newSetButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.newSetButton.setObjectName("newSetButton")
        self.horizontalLayout.addWidget(self.newSetButton)
        self.deleteSetButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.deleteSetButton.setObjectName("deleteSetButton")
        self.horizontalLayout.addWidget(self.deleteSetButton)
        self.favSetButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.favSetButton.setObjectName("favSetButton")
        self.horizontalLayout.addWidget(self.favSetButton)
        self.settingsTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.settingsTabWidget.setGeometry(QtCore.QRect(180, 20, 291, 311))
        self.settingsTabWidget.setObjectName("settingsTabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.dataTypeComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.dataTypeComboBox.setObjectName("dataTypeComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dataTypeComboBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.colorMapComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.colorMapComboBox.setObjectName("colorMapComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.colorMapComboBox)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scaleMinEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.scaleMinEdit.setObjectName("scaleMinEdit")
        self.horizontalLayout_2.addWidget(self.scaleMinEdit)
        self.scaleMaxEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.scaleMaxEdit.setObjectName("scaleMaxEdit")
        self.horizontalLayout_2.addWidget(self.scaleMaxEdit)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.settingsTabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.settingsTabWidget.addTab(self.tab_2, "")
        self.mainScreen = GraphicsLayoutWidget(self.centralwidget)
        self.mainScreen.setGeometry(QtCore.QRect(480, 10, 781, 631))
        self.mainScreen.setObjectName("mainScreen")
        self.metaDataBox = QtWidgets.QGroupBox(self.centralwidget)
        self.metaDataBox.setGeometry(QtCore.QRect(1270, 10, 191, 851))
        self.metaDataBox.setObjectName("metaDataBox")
        self.metaDataText = QtWidgets.QPlainTextEdit(self.metaDataBox)
        self.metaDataText.setGeometry(QtCore.QRect(0, 20, 191, 611))
        self.metaDataText.setObjectName("metaDataText")
        self.metaDataList = QtWidgets.QListWidget(self.metaDataBox)
        self.metaDataList.setGeometry(QtCore.QRect(0, 661, 191, 141))
        self.metaDataList.setObjectName("metaDataList")
        self.label_9 = QtWidgets.QLabel(self.metaDataBox)
        self.label_9.setGeometry(QtCore.QRect(3, 643, 161, 16))
        self.label_9.setObjectName("label_9")
        self.dataExplorerTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.dataExplorerTabWidget.setGeometry(QtCore.QRect(480, 650, 771, 211))
        self.dataExplorerTabWidget.setObjectName("dataExplorerTabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.tab_3)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 201, 58))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.quickPlotXComboBox = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.quickPlotXComboBox.setObjectName("quickPlotXComboBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.quickPlotXComboBox)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.quickPlotYComboBox = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.quickPlotYComboBox.setObjectName("quickPlotYComboBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.quickPlotYComboBox)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.quickPlotButton = QtWidgets.QPushButton(self.tab_3)
        self.quickPlotButton.setGeometry(QtCore.QRect(240, 20, 61, 51))
        self.quickPlotButton.setObjectName("quickPlotButton")
        self.dataExplorerTabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.dataExplorerTabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.dataExplorerTabWidget.addTab(self.tab_5, "")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1465, 22))
        self.menubar.setObjectName("menubar")
        self.menuDataView = QtWidgets.QMenu(self.menubar)
        self.menuDataView.setObjectName("menuDataView")
        self.menu2D = QtWidgets.QMenu(self.menuDataView)
        self.menu2D.setObjectName("menu2D")
        self.menu3D = QtWidgets.QMenu(self.menuDataView)
        self.menu3D.setObjectName("menu3D")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionv1s = QtWidgets.QAction(mainWindow)
        self.actionv1s.setObjectName("actionv1s")
        self.actionl = QtWidgets.QAction(mainWindow)
        self.actionl.setObjectName("actionl")
        self.menuDataView.addAction(self.menu2D.menuAction())
        self.menuDataView.addAction(self.menu3D.menuAction())
        self.menubar.addAction(self.menuDataView.menuAction())

        self.retranslateUi(mainWindow)
        self.settingsTabWidget.setCurrentIndex(0)
        self.dataExplorerTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "HAL"))
        self.dayBrowserBox.setTitle(_translate("mainWindow", "Day browser"))
        self.runBrowserBox.setTitle(_translate("mainWindow", "Run browser"))
        self.label_4.setText(_translate("mainWindow", "runs"))
        self.label_5.setText(_translate("mainWindow", "sequences"))
        self.label_6.setText(_translate("mainWindow", "sets"))
        self.refreshRunListButton.setText(_translate("mainWindow", "Refresh"))
        self.fitButton.setText(_translate("mainWindow", "FIT"))
        self.newSetButton.setText(_translate("mainWindow", "new"))
        self.deleteSetButton.setText(_translate("mainWindow", "del"))
        self.favSetButton.setText(_translate("mainWindow", "⭐"))
        self.label.setText(_translate("mainWindow", "Data Type"))
        self.label_2.setText(_translate("mainWindow", "Colormap"))
        self.label_3.setText(_translate("mainWindow", "Scale"))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.tab), _translate("mainWindow", "Data"))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.tab_2), _translate("mainWindow", "FIT"))
        self.metaDataBox.setTitle(_translate("mainWindow", "Meta Data"))
        self.label_9.setText(_translate("mainWindow", "Metadata sources :"))
        self.label_7.setText(_translate("mainWindow", "X :"))
        self.label_8.setText(_translate("mainWindow", "Y :"))
        self.quickPlotButton.setText(_translate("mainWindow", "PLOT"))
        self.dataExplorerTabWidget.setTabText(self.dataExplorerTabWidget.indexOf(self.tab_3), _translate("mainWindow", "Quick Plot"))
        self.dataExplorerTabWidget.setTabText(self.dataExplorerTabWidget.indexOf(self.tab_4), _translate("mainWindow", "Stats"))
        self.dataExplorerTabWidget.setTabText(self.dataExplorerTabWidget.indexOf(self.tab_5), _translate("mainWindow", "Advanced Plot"))
        self.menuDataView.setTitle(_translate("mainWindow", "Data View"))
        self.menu2D.setTitle(_translate("mainWindow", "2D"))
        self.menu3D.setTitle(_translate("mainWindow", "3D"))
        self.actionv1s.setText(_translate("mainWindow", "v1s"))
        self.actionl.setText(_translate("mainWindow", "l"))
from pyqtgraph import GraphicsLayoutWidget
