import random
import sys  # sys нужен для передачи argv в QApplication

import serial
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
import design  # Это наш конвертированный файл дизайна


class MindReaderApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.startButton.clicked.connect(self.start_timer)

        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        # настраиваем графики
        self.plot1 = self.graphic1.addPlot()
        self.curve1 = self.plot1.plot()

        self.plot2 = self.graphic2.addPlot()
        self.curve2 = self.plot2.plot()
        self.setGraphs()

        # задаем массивы для хранения данных
        self.data1 = []
        self.data2 = []
        self.timings = []
        self.counter = 0
        self.counter1 = 0

        # для кнопки
        self.clicked = False

        # настройка видео
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.chooseVideo.triggered.connect(self.openFile)
        self.videoChosed = False

        # настройка порта
        self.ser = serial.Serial()
        self.ser.baudrate = 57600
        self.port = ""
        self.choosePort.triggered.connect(self.inputCom)

    # запускает таймер, который работает сколько влезет, пауза кнопкой
    def start_timer(self):
        if self.clicked:
            self.startButton.setText("Запустить")
            self.timer.stop()
            self.timer.deleteLater()
            self.mediaPlayer.stop()
            self.clicked = False

            # show all in graphics
            xdict = dict(enumerate(self.timings))
            self.plot1.getAxis('bottom').setTicks([xdict.items()])
            self.curve1.setData(self.data1)
            self.plot2.getAxis('bottom').setTicks([xdict.items()])
            self.curve2.setData(self.data2)

        else:
            if self.port == "":
                QMessageBox.about(self, "Ошибка!", "Выберите COM порт!")
                return

            if not self.videoChosed:
                QMessageBox.about(self, "Ошибка!", "Выберите видеофайл для воспроизведения!")
                return

            self.startButton.setText("Остановить")
            self.counter = 0
            self.counter1 = 0

            self.time = QtCore.QTime(0, 0, 0)
            self.timer = QtCore.QTimer()

            #открытие порта
            self.ser.port = self.port
            if not self.ser.isOpen():
                self.ser.open()

            # reset data for graphs
            self.data1 = []
            self.data2 = []
            self.timings = []
            self.plot1.getAxis('bottom').setTicks([])
            self.plot2.getAxis('bottom').setTicks([])

            self.timer.timeout.connect(self.update)
            self.timer.start(4)

            self.mediaPlayer.play()
            self.clicked = True

    # то что происходит каждый тик таймера
    def update(self):

        self.counter += 1
        # заглушка для считываемого потока
        #x = random.randint(0, 100)
        #y = random.randint(0, 100)
        ########################

        #считка с устройства
        ch1, ch2 = self.readFromEEG()

        interval = 100 / 4
        # increase timings
        if self.counter >= interval:
            interval *= 4
            self.counter = 0
            self.counter1 += 1
            self.time = self.time.addMSecs(interval)
            self.timings.append(self.time.toString('mm:ss.zzz'))
            self.EmotionLabel.setText(str(ch1))
            self.updateGraphs(ch1, ch2)

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

    def updateGraphs(self, x, y):
        # increase first graph
        self.data1.append(x)

        numbp = 200
        # скорость прокрутки - выводятся последние numbp точек
        pos = int(self.counter1 - numbp)
        if pos < 0:
            pos = 0

        self.curve1.setData(self.data1[pos:self.counter1])
        xdict = dict(enumerate(self.timings[pos:self.counter1]))
        self.plot1.getAxis('bottom').setTicks([xdict.items()])
        self.plot1.setXRange(0, numbp)

        # increase second graph
        self.data2.append(y)

        self.curve2.setData(self.data2[pos:self.counter1])
        self.plot2.getAxis('bottom').setTicks([xdict.items()])
        self.plot2.setXRange(0, numbp)

    def openFile(self):
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                    QDir.homePath())

            if fileName != '':
                self.videoChosed = True
                self.mediaPlayer.setMedia(
                        QMediaContent(QUrl.fromLocalFile(fileName)))

    def readFromEEG(self):
        gotBegin = False

        # seek start
        while not gotBegin:

            # 1
            x = self.ser.read()
            while int.from_bytes(x, byteorder='big') != 165:
                x = self.ser.read()
            gotBegin = True

            # 2
            x = self.ser.read()
            gotBegin = gotBegin and int.from_bytes(x, byteorder='big') == 90

            # 3
            x = self.ser.read()
            gotBegin = gotBegin and int.from_bytes(x, byteorder='big') == 2

        # 4
        self.ser.read()

        def conv2sig(xb, yb):
            xi = int.from_bytes(xb, byteorder='big')
            yi = int.from_bytes(yb, byteorder='big')
            a = format(xi, 'b') + format(yi, 'b')
            return int(a, 2)

        # 5 and 6
        ch1 = conv2sig(self.ser.read(), self.ser.read())

        # 7 and 8
        ch2 = conv2sig(self.ser.read(), self.ser.read())

        return ch1, ch2

    def inputCom(self):

        text, ok = QInputDialog.getText(self, 'Выбор COM порта', 'Введите номер COM порта, к которому подключено устройство:')

        if ok:
            self.port = 'COM' + text

def main():
    #import pyqtgraph.examples
    #pyqtgraph.examples.run()

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MindReaderApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()