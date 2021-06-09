# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1335, 823)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browserColumn = QtWidgets.QVBoxLayout()
        self.browserColumn.setSpacing(1)
        self.browserColumn.setObjectName("browserColumn")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dayBrowserBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dayBrowserBox.sizePolicy().hasHeightForWidth())
        self.dayBrowserBox.setSizePolicy(sizePolicy)
        self.dayBrowserBox.setMaximumSize(QtCore.QSize(170, 500))
        self.dayBrowserBox.setObjectName("dayBrowserBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dayBrowserBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dayBrowserDateLayout = QtWidgets.QHBoxLayout()
        self.dayBrowserDateLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.dayBrowserDateLayout.setSpacing(1)
        self.dayBrowserDateLayout.setObjectName("dayBrowserDateLayout")
        self.dateEdit = QtWidgets.QDateEdit(self.dayBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setMinimumSize(QtCore.QSize(101, 0))
        self.dateEdit.setObjectName("dateEdit")
        self.dayBrowserDateLayout.addWidget(self.dateEdit)
        self.todayButton = QtWidgets.QPushButton(self.dayBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.todayButton.sizePolicy().hasHeightForWidth())
        self.todayButton.setSizePolicy(sizePolicy)
        self.todayButton.setMinimumSize(QtCore.QSize(41, 0))
        self.todayButton.setMaximumSize(QtCore.QSize(41, 16777215))
        self.todayButton.setObjectName("todayButton")
        self.dayBrowserDateLayout.addWidget(self.todayButton)
        self.verticalLayout.addLayout(self.dayBrowserDateLayout)
        self.dayBrowserListLayout = QtWidgets.QHBoxLayout()
        self.dayBrowserListLayout.setObjectName("dayBrowserListLayout")
        self.yearList = QtWidgets.QListWidget(self.dayBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yearList.sizePolicy().hasHeightForWidth())
        self.yearList.setSizePolicy(sizePolicy)
        self.yearList.setMinimumSize(QtCore.QSize(61, 0))
        self.yearList.setMaximumSize(QtCore.QSize(61, 16777215))
        self.yearList.setObjectName("yearList")
        self.dayBrowserListLayout.addWidget(self.yearList)
        self.monthList = QtWidgets.QListWidget(self.dayBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.monthList.sizePolicy().hasHeightForWidth())
        self.monthList.setSizePolicy(sizePolicy)
        self.monthList.setMinimumSize(QtCore.QSize(31, 0))
        self.monthList.setMaximumSize(QtCore.QSize(31, 16777215))
        self.monthList.setObjectName("monthList")
        self.dayBrowserListLayout.addWidget(self.monthList)
        self.dayList = QtWidgets.QListWidget(self.dayBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dayList.sizePolicy().hasHeightForWidth())
        self.dayList.setSizePolicy(sizePolicy)
        self.dayList.setMinimumSize(QtCore.QSize(31, 0))
        self.dayList.setMaximumSize(QtCore.QSize(31, 16777215))
        self.dayList.setObjectName("dayList")
        self.dayBrowserListLayout.addWidget(self.dayList)
        self.verticalLayout.addLayout(self.dayBrowserListLayout)
        self.horizontalLayout_3.addWidget(self.dayBrowserBox)
        self.settingsTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsTabWidget.sizePolicy().hasHeightForWidth())
        self.settingsTabWidget.setSizePolicy(sizePolicy)
        self.settingsTabWidget.setMaximumSize(QtCore.QSize(285, 16777215))
        self.settingsTabWidget.setObjectName("settingsTabWidget")
        self.settingsDataTab = QtWidgets.QWidget()
        self.settingsDataTab.setObjectName("settingsDataTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.settingsDataTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.settingsDataTab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.settingsDataTab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.scaleMinEdit = QtWidgets.QLineEdit(self.settingsDataTab)
        self.scaleMinEdit.setObjectName("scaleMinEdit")
        self.gridLayout_2.addWidget(self.scaleMinEdit, 2, 1, 1, 1)
        self.autoScaleCheckBox = QtWidgets.QCheckBox(self.settingsDataTab)
        self.autoScaleCheckBox.setTristate(False)
        self.autoScaleCheckBox.setObjectName("autoScaleCheckBox")
        self.gridLayout_2.addWidget(self.autoScaleCheckBox, 3, 0, 1, 1)
        self.scaleMaxEdit = QtWidgets.QLineEdit(self.settingsDataTab)
        self.scaleMaxEdit.setObjectName("scaleMaxEdit")
        self.gridLayout_2.addWidget(self.scaleMaxEdit, 2, 2, 1, 1)
        self.colorMapComboBox = QtWidgets.QComboBox(self.settingsDataTab)
        self.colorMapComboBox.setObjectName("colorMapComboBox")
        self.gridLayout_2.addWidget(self.colorMapComboBox, 1, 1, 1, 2)
        self.dataTypeComboBox = QtWidgets.QComboBox(self.settingsDataTab)
        self.dataTypeComboBox.setObjectName("dataTypeComboBox")
        self.gridLayout_2.addWidget(self.dataTypeComboBox, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.settingsDataTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.settingsTabWidget.addTab(self.settingsDataTab, "")
        self.settingsFitTab = QtWidgets.QWidget()
        self.settingsFitTab.setObjectName("settingsFitTab")
        self.fitButton = QtWidgets.QPushButton(self.settingsFitTab)
        self.fitButton.setGeometry(QtCore.QRect(10, 180, 101, 41))
        self.fitButton.setObjectName("fitButton")
        self.label_10 = QtWidgets.QLabel(self.settingsFitTab)
        self.label_10.setGeometry(QtCore.QRect(130, 170, 51, 23))
        self.label_10.setObjectName("label_10")
        self.selectRoiComboBox = QtWidgets.QComboBox(self.settingsFitTab)
        self.selectRoiComboBox.setGeometry(QtCore.QRect(120, 20, 151, 23))
        self.selectRoiComboBox.setObjectName("selectRoiComboBox")
        self.addRoiButton = QtWidgets.QPushButton(self.settingsFitTab)
        self.addRoiButton.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.addRoiButton.setObjectName("addRoiButton")
        self.fitTypeComboBox = QtWidgets.QComboBox(self.settingsFitTab)
        self.fitTypeComboBox.setGeometry(QtCore.QRect(130, 190, 121, 23))
        self.fitTypeComboBox.setObjectName("fitTypeComboBox")
        self.backgroundCheckBox = QtWidgets.QCheckBox(self.settingsFitTab)
        self.backgroundCheckBox.setGeometry(QtCore.QRect(10, 140, 101, 21))
        self.backgroundCheckBox.setObjectName("backgroundCheckBox")
        self.deleteRoiButton = QtWidgets.QPushButton(self.settingsFitTab)
        self.deleteRoiButton.setGeometry(QtCore.QRect(10, 70, 91, 23))
        self.deleteRoiButton.setObjectName("deleteRoiButton")
        self.resetRoiButton = QtWidgets.QPushButton(self.settingsFitTab)
        self.resetRoiButton.setGeometry(QtCore.QRect(10, 100, 91, 23))
        self.resetRoiButton.setObjectName("resetRoiButton")
        self.renameRoiButton = QtWidgets.QPushButton(self.settingsFitTab)
        self.renameRoiButton.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.renameRoiButton.setObjectName("renameRoiButton")
        self.label_11 = QtWidgets.QLabel(self.settingsFitTab)
        self.label_11.setGeometry(QtCore.QRect(120, 0, 71, 23))
        self.label_11.setObjectName("label_11")
        self.settingsTabWidget.addTab(self.settingsFitTab, "")
        self.horizontalLayout_3.addWidget(self.settingsTabWidget)
        self.browserColumn.addLayout(self.horizontalLayout_3)
        self.runBrowserBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runBrowserBox.sizePolicy().hasHeightForWidth())
        self.runBrowserBox.setSizePolicy(sizePolicy)
        self.runBrowserBox.setMaximumSize(QtCore.QSize(460, 16777215))
        self.runBrowserBox.setObjectName("runBrowserBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.runBrowserBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.runList = QtWidgets.QListWidget(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runList.sizePolicy().hasHeightForWidth())
        self.runList.setSizePolicy(sizePolicy)
        self.runList.setObjectName("runList")
        self.gridLayout.addWidget(self.runList, 1, 0, 1, 1)
        self.seqList = QtWidgets.QListWidget(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seqList.sizePolicy().hasHeightForWidth())
        self.seqList.setSizePolicy(sizePolicy)
        self.seqList.setObjectName("seqList")
        self.gridLayout.addWidget(self.seqList, 1, 1, 1, 1)
        self.setList = QtWidgets.QListWidget(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setList.sizePolicy().hasHeightForWidth())
        self.setList.setSizePolicy(sizePolicy)
        self.setList.setObjectName("setList")
        self.gridLayout.addWidget(self.setList, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.refreshRunListButton = QtWidgets.QPushButton(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshRunListButton.sizePolicy().hasHeightForWidth())
        self.refreshRunListButton.setSizePolicy(sizePolicy)
        self.refreshRunListButton.setObjectName("refreshRunListButton")
        self.horizontalLayout_5.addWidget(self.refreshRunListButton)
        self.fitBrowserButton = QtWidgets.QPushButton(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fitBrowserButton.sizePolicy().hasHeightForWidth())
        self.fitBrowserButton.setSizePolicy(sizePolicy)
        self.fitBrowserButton.setObjectName("fitBrowserButton")
        self.horizontalLayout_5.addWidget(self.fitBrowserButton)
        self.deleteFitButton = QtWidgets.QPushButton(self.runBrowserBox)
        self.deleteFitButton.setObjectName("deleteFitButton")
        self.horizontalLayout_5.addWidget(self.deleteFitButton)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.newSetButton = QtWidgets.QPushButton(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newSetButton.sizePolicy().hasHeightForWidth())
        self.newSetButton.setSizePolicy(sizePolicy)
        self.newSetButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.newSetButton.setObjectName("newSetButton")
        self.horizontalLayout_4.addWidget(self.newSetButton)
        self.deleteSetButton = QtWidgets.QPushButton(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteSetButton.sizePolicy().hasHeightForWidth())
        self.deleteSetButton.setSizePolicy(sizePolicy)
        self.deleteSetButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.deleteSetButton.setObjectName("deleteSetButton")
        self.horizontalLayout_4.addWidget(self.deleteSetButton)
        self.favSetButton = QtWidgets.QPushButton(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.favSetButton.sizePolicy().hasHeightForWidth())
        self.favSetButton.setSizePolicy(sizePolicy)
        self.favSetButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.favSetButton.setObjectName("favSetButton")
        self.horizontalLayout_4.addWidget(self.favSetButton)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.progressBar = QtWidgets.QProgressBar(self.runBrowserBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 20))
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.debugButton = QtWidgets.QPushButton(self.runBrowserBox)
        self.debugButton.setMinimumSize(QtCore.QSize(0, 50))
        self.debugButton.setObjectName("debugButton")
        self.verticalLayout_2.addWidget(self.debugButton)
        self.browserColumn.addWidget(self.runBrowserBox)
        self.horizontalLayout.addLayout(self.browserColumn)
        self.screenColumn = QtWidgets.QVBoxLayout()
        self.screenColumn.setObjectName("screenColumn")
        self.mainScreen = GraphicsLayoutWidget(self.centralwidget)
        self.mainScreen.setObjectName("mainScreen")
        self.screenColumn.addWidget(self.mainScreen)
        self.dataAnalysisTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.dataAnalysisTabWidget.setMaximumSize(QtCore.QSize(16777215, 220))
        self.dataAnalysisTabWidget.setObjectName("dataAnalysisTabWidget")
        self.quickAnalysisTab = QtWidgets.QWidget()
        self.quickAnalysisTab.setObjectName("quickAnalysisTab")
        self.quickPlotButton = QtWidgets.QPushButton(self.quickAnalysisTab)
        self.quickPlotButton.setGeometry(QtCore.QRect(230, 20, 61, 51))
        self.quickPlotButton.setObjectName("quickPlotButton")
        self.quickStatsButton = QtWidgets.QPushButton(self.quickAnalysisTab)
        self.quickStatsButton.setGeometry(QtCore.QRect(300, 20, 61, 51))
        self.quickStatsButton.setObjectName("quickStatsButton")
        self.formLayoutWidget = QtWidgets.QWidget(self.quickAnalysisTab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 191, 51))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(5)
        self.formLayout.setObjectName("formLayout")
        self.quickPlotXToolButton = QtWidgets.QToolButton(self.formLayoutWidget)
        self.quickPlotXToolButton.setObjectName("quickPlotXToolButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.quickPlotXToolButton)
        self.quickPlotYToolButton = QtWidgets.QToolButton(self.formLayoutWidget)
        self.quickPlotYToolButton.setObjectName("quickPlotYToolButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.quickPlotYToolButton)
        self.quickPlotXLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.quickPlotXLabel.setObjectName("quickPlotXLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.quickPlotXLabel)
        self.quickPlotYLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.quickPlotYLabel.setObjectName("quickPlotYLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.quickPlotYLabel)
        self.dataAnalysisTabWidget.addTab(self.quickAnalysisTab, "")
        self.advancedAnalysisTab = QtWidgets.QWidget()
        self.advancedAnalysisTab.setObjectName("advancedAnalysisTab")
        self.variableDeclarationTable = QtWidgets.QTableWidget(self.advancedAnalysisTab)
        self.variableDeclarationTable.setGeometry(QtCore.QRect(10, 32, 250, 151))
        self.variableDeclarationTable.setObjectName("variableDeclarationTable")
        self.variableDeclarationTable.setColumnCount(0)
        self.variableDeclarationTable.setRowCount(0)
        self.subplotContentTable = QtWidgets.QTableWidget(self.advancedAnalysisTab)
        self.subplotContentTable.setGeometry(QtCore.QRect(489, 32, 271, 151))
        self.subplotContentTable.setObjectName("subplotContentTable")
        self.subplotContentTable.setColumnCount(0)
        self.subplotContentTable.setRowCount(0)
        self.subplotSetupTable = QtWidgets.QTableWidget(self.advancedAnalysisTab)
        self.subplotSetupTable.setGeometry(QtCore.QRect(280, 32, 191, 101))
        self.subplotSetupTable.setObjectName("subplotSetupTable")
        self.subplotSetupTable.setColumnCount(0)
        self.subplotSetupTable.setRowCount(0)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.advancedAnalysisTab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 339, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.advancedPlotSelectionBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.advancedPlotSelectionBox.setObjectName("advancedPlotSelectionBox")
        self.horizontalLayout_2.addWidget(self.advancedPlotSelectionBox)
        self.advancedPlotSaveButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.advancedPlotSaveButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.advancedPlotSaveButton.setObjectName("advancedPlotSaveButton")
        self.horizontalLayout_2.addWidget(self.advancedPlotSaveButton)
        self.advancedPlotSaveAsButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.advancedPlotSaveAsButton.setMaximumSize(QtCore.QSize(70, 16777215))
        self.advancedPlotSaveAsButton.setObjectName("advancedPlotSaveAsButton")
        self.horizontalLayout_2.addWidget(self.advancedPlotSaveAsButton)
        self.advancedPlotDeleteButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.advancedPlotDeleteButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.advancedPlotDeleteButton.setObjectName("advancedPlotDeleteButton")
        self.horizontalLayout_2.addWidget(self.advancedPlotDeleteButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.advancedAnalysisTab)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(500, 0, 259, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.advancedStatButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.advancedStatButton.setObjectName("advancedStatButton")
        self.horizontalLayout_7.addWidget(self.advancedStatButton)
        self.exportDataButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.exportDataButton.setObjectName("exportDataButton")
        self.horizontalLayout_7.addWidget(self.exportDataButton)
        self.exportToMatplotlibButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.exportToMatplotlibButton.setObjectName("exportToMatplotlibButton")
        self.horizontalLayout_7.addWidget(self.exportToMatplotlibButton)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.advancedAnalysisTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(280, 130, 191, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.updateSubplotLayoutButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.updateSubplotLayoutButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.updateSubplotLayoutButton.setObjectName("updateSubplotLayoutButton")
        self.horizontalLayout_8.addWidget(self.updateSubplotLayoutButton)
        self.resetSubplotLayoutButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.resetSubplotLayoutButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.resetSubplotLayoutButton.setObjectName("resetSubplotLayoutButton")
        self.horizontalLayout_8.addWidget(self.resetSubplotLayoutButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.advancedPlotResetButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.advancedPlotResetButton.setObjectName("advancedPlotResetButton")
        self.horizontalLayout_10.addWidget(self.advancedPlotResetButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.dataAnalysisTabWidget.addTab(self.advancedAnalysisTab, "")
        self.screenColumn.addWidget(self.dataAnalysisTabWidget)
        self.horizontalLayout.addLayout(self.screenColumn)
        self.metaColumn = QtWidgets.QVBoxLayout()
        self.metaColumn.setObjectName("metaColumn")
        self.metaDataText = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.metaDataText.sizePolicy().hasHeightForWidth())
        self.metaDataText.setSizePolicy(sizePolicy)
        self.metaDataText.setObjectName("metaDataText")
        self.metaColumn.addWidget(self.metaDataText)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.metaColumn.addWidget(self.label_7)
        self.metaDataList = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.metaDataList.sizePolicy().hasHeightForWidth())
        self.metaDataList.setSizePolicy(sizePolicy)
        self.metaDataList.setMinimumSize(QtCore.QSize(0, 0))
        self.metaDataList.setMaximumSize(QtCore.QSize(240, 140))
        self.metaDataList.setObjectName("metaDataList")
        self.metaColumn.addWidget(self.metaDataList)
        self.refreshMetadataCachebutton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshMetadataCachebutton.setObjectName("refreshMetadataCachebutton")
        self.metaColumn.addWidget(self.refreshMetadataCachebutton)
        self.horizontalLayout.addLayout(self.metaColumn)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1335, 20))
        self.menubar.setObjectName("menubar")
        self.menuDataDisplay = QtWidgets.QMenu(self.menubar)
        self.menuDataDisplay.setObjectName("menuDataDisplay")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionv1s = QtWidgets.QAction(mainWindow)
        self.actionv1s.setObjectName("actionv1s")
        self.actionl = QtWidgets.QAction(mainWindow)
        self.actionl.setObjectName("actionl")
        self.actionlol = QtWidgets.QAction(mainWindow)
        self.actionlol.setObjectName("actionlol")
        self.menubar.addAction(self.menuDataDisplay.menuAction())

        self.retranslateUi(mainWindow)
        self.settingsTabWidget.setCurrentIndex(0)
        self.dataAnalysisTabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "HAL"))
        self.dayBrowserBox.setTitle(_translate("mainWindow", "Day Browser"))
        self.todayButton.setText(_translate("mainWindow", "now"))
        self.label.setText(_translate("mainWindow", "Data Type"))
        self.label_3.setText(_translate("mainWindow", "Scale"))
        self.autoScaleCheckBox.setText(_translate("mainWindow", "auto"))
        self.label_2.setText(_translate("mainWindow", "Colormap"))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.settingsDataTab), _translate("mainWindow", "Data"))
        self.fitButton.setText(_translate("mainWindow", "FIT"))
        self.label_10.setText(_translate("mainWindow", "fit type:"))
        self.addRoiButton.setText(_translate("mainWindow", "add ROI"))
        self.backgroundCheckBox.setText(_translate("mainWindow", "background"))
        self.deleteRoiButton.setText(_translate("mainWindow", "Delete ROI"))
        self.resetRoiButton.setText(_translate("mainWindow", "Reset ROIs"))
        self.renameRoiButton.setText(_translate("mainWindow", "Rename ROI"))
        self.label_11.setText(_translate("mainWindow", "select ROI:"))
        self.settingsTabWidget.setTabText(self.settingsTabWidget.indexOf(self.settingsFitTab), _translate("mainWindow", "FIT"))
        self.runBrowserBox.setTitle(_translate("mainWindow", "Run Browser"))
        self.label_4.setText(_translate("mainWindow", "runs"))
        self.label_5.setText(_translate("mainWindow", "sequences"))
        self.label_6.setText(_translate("mainWindow", "sets"))
        self.refreshRunListButton.setText(_translate("mainWindow", "Refresh"))
        self.fitBrowserButton.setText(_translate("mainWindow", "FIT"))
        self.deleteFitButton.setText(_translate("mainWindow", "Del. Fit"))
        self.newSetButton.setText(_translate("mainWindow", "new"))
        self.deleteSetButton.setText(_translate("mainWindow", "del"))
        self.favSetButton.setText(_translate("mainWindow", "⭐"))
        self.debugButton.setText(_translate("mainWindow", "DEBUG"))
        self.quickPlotButton.setText(_translate("mainWindow", "PLOT"))
        self.quickStatsButton.setText(_translate("mainWindow", "STATS"))
        self.quickPlotXToolButton.setText(_translate("mainWindow", "X"))
        self.quickPlotYToolButton.setText(_translate("mainWindow", "Y"))
        self.quickPlotXLabel.setText(_translate("mainWindow", "quickPlotXLabel"))
        self.quickPlotYLabel.setText(_translate("mainWindow", "quickPlotYLabel"))
        self.dataAnalysisTabWidget.setTabText(self.dataAnalysisTabWidget.indexOf(self.quickAnalysisTab), _translate("mainWindow", "Quick Analysis"))
        self.advancedPlotSaveButton.setText(_translate("mainWindow", "save"))
        self.advancedPlotSaveAsButton.setText(_translate("mainWindow", "save as..."))
        self.advancedPlotDeleteButton.setText(_translate("mainWindow", "delete"))
        self.advancedStatButton.setText(_translate("mainWindow", "STATS"))
        self.exportDataButton.setText(_translate("mainWindow", "export"))
        self.exportToMatplotlibButton.setText(_translate("mainWindow", "to matplotlib"))
        self.label_8.setText(_translate("mainWindow", "layout"))
        self.updateSubplotLayoutButton.setText(_translate("mainWindow", "update"))
        self.resetSubplotLayoutButton.setText(_translate("mainWindow", "reset"))
        self.advancedPlotResetButton.setText(_translate("mainWindow", "reset all"))
        self.dataAnalysisTabWidget.setTabText(self.dataAnalysisTabWidget.indexOf(self.advancedAnalysisTab), _translate("mainWindow", "Advanced Analysis"))
        self.label_7.setText(_translate("mainWindow", "Metadata sources:"))
        self.refreshMetadataCachebutton.setText(_translate("mainWindow", "refresh metadata cache"))
        self.menuDataDisplay.setTitle(_translate("mainWindow", "Data Display"))
        self.actionv1s.setText(_translate("mainWindow", "v1s"))
        self.actionl.setText(_translate("mainWindow", "l"))
        self.actionlol.setText(_translate("mainWindow", "lol"))
from pyqtgraph import GraphicsLayoutWidget
