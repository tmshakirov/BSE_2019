# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(322, 455)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 10, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.emotionsView = QtWidgets.QListView(self.centralwidget)
        self.emotionsView.setGeometry(QtCore.QRect(10, 40, 291, 181))
        self.emotionsView.setObjectName("emotionsView")
        self.emotionName = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionName.setGeometry(QtCore.QRect(170, 240, 131, 20))
        self.emotionName.setObjectName("emotionName")
        self.emotionLabel = QtWidgets.QLabel(self.centralwidget)
        self.emotionLabel.setGeometry(QtCore.QRect(10, 240, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionLabel.setFont(font)
        self.emotionLabel.setObjectName("emotionLabel")
        self.emotionStrengthLabel = QtWidgets.QLabel(self.centralwidget)
        self.emotionStrengthLabel.setGeometry(QtCore.QRect(10, 270, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionStrengthLabel.setFont(font)
        self.emotionStrengthLabel.setObjectName("emotionStrengthLabel")
        self.emotionColorLabel = QtWidgets.QLabel(self.centralwidget)
        self.emotionColorLabel.setGeometry(QtCore.QRect(10, 300, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionColorLabel.setFont(font)
        self.emotionColorLabel.setObjectName("emotionColorLabel")
        self.emotionStrength1 = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionStrength1.setGeometry(QtCore.QRect(190, 270, 41, 20))
        self.emotionStrength1.setObjectName("emotionStrength1")
        self.emotionColor1 = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionColor1.setGeometry(QtCore.QRect(190, 300, 41, 20))
        self.emotionColor1.setObjectName("emotionColor1")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(10, 340, 130, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.emotionStrength2 = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionStrength2.setGeometry(QtCore.QRect(260, 270, 41, 20))
        self.emotionStrength2.setObjectName("emotionStrength2")
        self.emotionColor2 = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionColor2.setGeometry(QtCore.QRect(260, 300, 41, 20))
        self.emotionColor2.setObjectName("emotionColor2")
        self.emotionStrengthLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.emotionStrengthLabel_2.setGeometry(QtCore.QRect(170, 270, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionStrengthLabel_2.setFont(font)
        self.emotionStrengthLabel_2.setObjectName("emotionStrengthLabel_2")
        self.emotionStrengthLabel_3 = QtWidgets.QLabel(self.centralwidget)
        self.emotionStrengthLabel_3.setGeometry(QtCore.QRect(170, 300, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionStrengthLabel_3.setFont(font)
        self.emotionStrengthLabel_3.setObjectName("emotionStrengthLabel_3")
        self.emotionStrengthLabel_4 = QtWidgets.QLabel(self.centralwidget)
        self.emotionStrengthLabel_4.setGeometry(QtCore.QRect(240, 270, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionStrengthLabel_4.setFont(font)
        self.emotionStrengthLabel_4.setObjectName("emotionStrengthLabel_4")
        self.emotionStrengthLabel_5 = QtWidgets.QLabel(self.centralwidget)
        self.emotionStrengthLabel_5.setGeometry(QtCore.QRect(240, 300, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.emotionStrengthLabel_5.setFont(font)
        self.emotionStrengthLabel_5.setObjectName("emotionStrengthLabel_5")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(180, 340, 130, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(80, 390, 150, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Список эмоций"))
        self.emotionLabel.setText(_translate("MainWindow", "Название эмоции"))
        self.emotionStrengthLabel.setText(_translate("MainWindow", "Сила эмоции"))
        self.emotionColorLabel.setText(_translate("MainWindow", "Окраска эмоции"))
        self.addButton.setText(_translate("MainWindow", "Добавить эмоцию"))
        self.emotionStrengthLabel_2.setText(_translate("MainWindow", "от"))
        self.emotionStrengthLabel_3.setText(_translate("MainWindow", "от"))
        self.emotionStrengthLabel_4.setText(_translate("MainWindow", "до"))
        self.emotionStrengthLabel_5.setText(_translate("MainWindow", "до"))
        self.deleteButton.setText(_translate("MainWindow", "Удалить эмоцию"))
        self.saveButton.setText(_translate("MainWindow", "Сохранить настройки"))

