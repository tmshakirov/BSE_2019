import random
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QAction

import design  # Это наш конвертированный файл дизайна
import pyqtgraph as pg
import numpy as np

class MindReaderApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.startButton.clicked.connect(lambda: self.start_timer(10, 100))

        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        class TimeAxisItem(pg.AxisItem):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def tickStrings(self, values, scale, spacing):
                # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
                return [QtCore.QTime().addMSecs(value).toString('mm:ss.zzz') for value in values]

        # настраиваем графики
        self.plot1 = self.graphic1.addPlot(title='Timed data', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.curve1 = self.plot1.plot()

        self.plot2 = self.graphic2.addPlot()
        self.curve2 = self.plot2.plot()
        self.setGraphs()

        # задаем массивы для хранения данных
        self.data1 = []
        self.data2 = []
        self.timings = []

        # для кнопки
        self.clicked = False

        # настройка видео
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.chooseVideo.triggered.connect(self.openFile)


    # запускает таймер, который работает заданное количество секунд
    def start_timer(self, seconds=10, interval=10):

        if self.clicked:
            self.startButton.setText("Запустить")
            self.timer.stop()
            self.timer.deleteLater()

            self.mediaPlayer.stop()
            self.clicked = False

            # reset data for graphs
            self.data1 = []
            self.data2 = []
            self.timings = []

            self.plot1.getAxis('bottom').setTicks([])
            self.plot2.getAxis('bottom').setTicks([])
        else:
            self.startButton.setText("Остановить")
            counter = 0
            count = seconds * 1000 / interval

            self.time = QtCore.QTime(0, 0, 0)
            self.timer = QtCore.QTimer()

            def handler():
                nonlocal counter
                counter += 1
                self.update(counter, interval)
                #if counter >= count:
                    #self.timer.stop()
                    #self.timer.deleteLater()

            self.timer.timeout.connect(handler)
            self.timer.start(interval)

            self.mediaPlayer.play()
            self.clicked = True

    # то что происходит каждый тик таймера
    def update(self, counter, interval):

        # заглушка для считываемого потока
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        ########################

        # increase timings
        self.time = self.time.addMSecs(interval)
        self.timings.append(self.time.toString('mm:ss.zzz'))

        self.EmotionLabel.setText(self.time.toString('mm:ss.zzz'))
        self.updateGraphs(x, y, interval, counter)

    def setGraphs(self):
        # self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        # Use automatic downsampling and clipping to reduce the drawing load
        self.plot1.setDownsampling(mode='peak')
        self.plot1.setClipToView(True)
        self.plot1.setRange(xRange=[0, 100])
        self.plot1.setLimits(xMin=0)

        self.plot2.setDownsampling(mode='peak')
        self.plot2.setClipToView(True)
        self.plot2.setRange(xRange=[0, 100])
        self.plot2.setLimits(xMin=0)


    def updateGraphs(self, x, y, interval, counter):
        # increase first graph
        self.data1.append(x)

        xdict = dict(enumerate(self.timings))
        xax = self.plot1.getAxis('bottom')
        xax.setTicks([xdict.items()])

        self.curve1.setData(y=self.data1)

        # скорость прокрутки - выводится последние 10 секунд
        self.plot1.setXRange(counter - 10000/interval, counter - 10)


        # increase second graph
        self.data2.append(y)

        xdict = dict(enumerate(self.timings))
        xax1 = self.plot2.getAxis('bottom')
        xax1.setTicks([xdict.items()])

        self.curve2.setData(y=self.data2)
        # скорость прокрутки - выводится последние 10 секунд
        self.plot2.setXRange(counter - 10000 / interval, counter - 10)


    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))

def main():
    #import pyqtgraph.examples
    #pyqtgraph.examples.run()

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MindReaderApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()