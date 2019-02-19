# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Project.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1789, 864)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(10, 780, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.EmotionLabel = QtWidgets.QLabel(self.centralwidget)
        self.EmotionLabel.setGeometry(QtCore.QRect(10, 20, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.EmotionLabel.setFont(font)
        self.EmotionLabel.setObjectName("EmotionLabel")
        self.graphic1 = GraphicsLayoutWidget(self.centralwidget)
        self.graphic1.setGeometry(QtCore.QRect(1170, 40, 611, 361))
        self.graphic1.setObjectName("graphic1")
        self.graphic2 = GraphicsLayoutWidget(self.centralwidget)
        self.graphic2.setGeometry(QtCore.QRect(1170, 460, 611, 361))
        self.graphic2.setObjectName("graphic2")
        self.graphLabel1 = QtWidgets.QLabel(self.centralwidget)
        self.graphLabel1.setEnabled(True)
        self.graphLabel1.setGeometry(QtCore.QRect(1170, 10, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.graphLabel1.setFont(font)
        self.graphLabel1.setObjectName("graphLabel1")
        self.graphLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.graphLabel2.setEnabled(True)
        self.graphLabel2.setGeometry(QtCore.QRect(1170, 430, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.graphLabel2.setFont(font)
        self.graphLabel2.setObjectName("graphLabel2")
        self.videoWidget = QVideoWidget(self.centralwidget)
        self.videoWidget.setGeometry(QtCore.QRect(10, 50, 1121, 711))
        self.videoWidget.setObjectName("videoWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1789, 21))
        self.menubar.setObjectName("menubar")
        self.openPrevSession = QtWidgets.QMenu(self.menubar)
        self.openPrevSession.setObjectName("openPrevSession")
        self.settings = QtWidgets.QMenu(self.menubar)
        self.settings.setObjectName("settings")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.choosePort = QtWidgets.QAction(MainWindow)
        self.choosePort.setObjectName("choosePort")
        self.setEmotions = QtWidgets.QAction(MainWindow)
        self.setEmotions.setObjectName("setEmotions")
        self.chooseVideo = QtWidgets.QAction(MainWindow)
        self.chooseVideo.setObjectName("chooseVideo")
        self.setUser = QtWidgets.QAction(MainWindow)
        self.setUser.setObjectName("setUser")
        self.settings.addAction(self.setUser)
        self.settings.addAction(self.setEmotions)
        self.settings.addAction(self.chooseVideo)
        self.settings.addAction(self.choosePort)
        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.openPrevSession.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startButton.setText(_translate("MainWindow", "Запуск"))
        self.EmotionLabel.setText(_translate("MainWindow", "Эмоция:"))
        self.graphLabel1.setText(_translate("MainWindow", "Окраска эмоции"))
        self.graphLabel2.setText(_translate("MainWindow", "Сила эмоции"))
        self.openPrevSession.setTitle(_translate("MainWindow", "Загрузить предыдущую сессию работы"))
        self.settings.setTitle(_translate("MainWindow", "Настройки"))
        self.action.setText(_translate("MainWindow", "Загрузить предыдущую сессию"))
        self.choosePort.setText(_translate("MainWindow", "Выбрать порт"))
        self.setEmotions.setText(_translate("MainWindow", "Настроить определяемые эмоции"))
        self.chooseVideo.setText(_translate("MainWindow", "Выбрать видеофайл"))
        self.setUser.setText(_translate("MainWindow", "Настроить данные пользователя"))


from PyQt5.QtMultimediaWidgets import QVideoWidget
from pyqtgraph import GraphicsLayoutWidget
