# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(322, 403)
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
        self.emotionStrength = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionStrength.setGeometry(QtCore.QRect(170, 270, 131, 20))
        self.emotionStrength.setObjectName("emotionStrength")
        self.emotionColor = QtWidgets.QLineEdit(self.centralwidget)
        self.emotionColor.setGeometry(QtCore.QRect(170, 300, 131, 20))
        self.emotionColor.setObjectName("emotionColor")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(70, 340, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
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


