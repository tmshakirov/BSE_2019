import os
import random
import sys  # sys нужен для передачи argv в QApplication

import serial
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QAction
import design  # Это наш конвертированный файл дизайна
import settingsdesign  # Файл дизайна настроек

class MindReaderApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.setWindowTitle("MindReader")

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
        self.emotions = []
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

        # файл
        self.fname = 'previousSession.emtn'
        if not os.path.isfile(self.fname):
            self.f = open(self.fname, 'w')
            self.f.close()
        self.vidFileName = ""
        self.f = open(self.fname, 'r')

        # для считки
        self.fromFile = False
        act = QAction("Выбрать файл", self)
        act.triggered.connect(self.loadFile)
        self.openPrevSession.addAction(act)

        act1 = QAction("Очистить", self)
        act1.triggered.connect(self.cancel)
        self.openPrevSession.addAction(act1)

        # файл настроек
        self.sname = 'settings.txt'
        self.emotions = []
        if not os.path.isfile(self.sname):
            self.f = open(self.sname, 'w')
            self.f.close()
        self.f = open(self.sname, 'r')

        #для считки настроек из файла
        self.settings.addAction(self.setEmotions)
        self.setEmotionsData.triggered.connect(self.loadSettings)

        # эмоции
        self.settings = SettingsWindow()
        self.setEmotions.triggered.connect(self.openSettings)
        self.emotionsList = []

    def cancel(self):
        self.fromFile = False

    def stop(self):
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

        # close file
        self.f.close()

    # запускает таймер, который работает сколько влезет, пауза кнопкой
    def start_timer(self):
        if self.clicked:
            self.stop()

        else:
            if not self.fromFile:

                if self.port == "":
                    QMessageBox.about(self, "Ошибка!", "Выберите COM порт!")
                    return

                if not self.videoChosed:
                    QMessageBox.about(self, "Ошибка!", "Выберите видеофайл для воспроизведения!")
                    return

                # открытие порта
                self.ser.port = self.port
                if not self.ser.isOpen():
                    try:
                        self.ser.open()
                    except serial.SerialException:
                        QMessageBox.about(self, "Ошибка!", "Выберите работающий COM порт!")
                        return

                # reset data for graphs
                self.data1 = []
                self.data2 = []
                self.timings = []
                self.emotions = []
                self.plot1.getAxis('bottom').setTicks([])
                self.plot2.getAxis('bottom').setTicks([])

                # new file
                path, _ = QFileDialog.getSaveFileName(self, "Сохранить сессию",
                                                                  QDir.homePath(), "Emotion Files (*.emtn)")
                if path != '':
                    self.f = open(path, 'w+')
                    self.f.write(self.vidFileName + "\n")
            self.startButton.setText("Остановить")
            self.counter = 0
            self.counter1 = 0

            self.emotionsList = self.settings.emotions
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.vidFileName)))

            self.time = QtCore.QTime(0, 0, 0)
            self.timer = QtCore.QTimer()

            self.timer.timeout.connect(self.update)
            self.timer.start(4)

            self.mediaPlayer.play()
            self.clicked = True

    # то что происходит каждый тик таймера
    def update(self):

        self.counter += 1

        if not self.fromFile:

            # заглушка для считываемого потока
            # ch1 = random.randint(0, 10)
            # ch2 = random.randint(0, 10)
            ########################

            # считка с устройства
            ch1, ch2 = self.readFromEEG()

            # получаем эмоцию
            emtn = self.getEmotion(ch1, ch2)

        # точки выводятся каждые 100 мс
        interval = 100 / 4
        if self.counter >= interval:
            interval *= 4
            self.counter = 0

            # добавляем точки только если их надо считывать
            if not self.fromFile:
                self.time = self.time.addMSecs(interval)
                self.timings.append(self.time.toString('mm:ss.zzz'))
                self.emotions.append(emtn)
                self.data1.append(ch1)
                self.data2.append(ch2)

                # запись в файл
                self.f.write(str(ch1) + "|" + str(ch2) + "|" + self.time.toString('mm:ss.zzz') + "|" + emtn + "\n")

            # все отображается по готовому набору данных и прокручивается каунтером1
            self.EmotionLabel.setText("Текущая эмоция: " + self.emotions[self.counter1])
            self.updateGraphs()
            self.counter1 += 1

            # если все данные уже показаны то стоп
            if self.fromFile and self.counter1 >= len(self.data1):
                self.stop()

    def updateGraphs(self):

        numbp = 200
        # скорость прокрутки - выводятся последние numbp точек
        pos = int(self.counter1 - numbp)
        if pos < 0:
            pos = 0

        xdict = dict(enumerate(self.timings[pos:self.counter1]))

        self.curve1.setData(self.data1[pos:self.counter1])
        self.plot1.getAxis('bottom').setTicks([xdict.items()])
        self.plot1.setXRange(0, numbp)

        self.curve2.setData(self.data2[pos:self.counter1])
        self.plot2.getAxis('bottom').setTicks([xdict.items()])
        self.plot2.setXRange(0, numbp)

    def getEmotion(self, ch1, ch2):

        for emt in self.emotionsList:
            isRight = False
            if emt.from_strength <= ch1 <= emt.to_strength:
                if emt.from_color <= ch2 <= emt.to_color:
                    isRight = True

            if isRight:
                return emt.name

        return "не определена"

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

    def openFile(self):
            self.vidFileName, _ = QFileDialog.getOpenFileName(self, "Открыть видео",
                    QDir.homePath())

            if self.vidFileName != '':
                self.videoChosed = True

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

            self.ser.port = self.port
            if not self.ser.isOpen():
                try:
                    self.ser.open()
                except serial.SerialException:
                    QMessageBox.about(self, "Ошибка!", "Выберите работающий COM порт!")

    def loadFile(self):

        try:
            path, _ = QFileDialog.getOpenFileName(self, "Открыть файл",
                                                          QDir.homePath(), "Emotion Files (*.emtn)")
            if path != '':
                self.fromFile = True
                f = open(path, 'r')

                allLines = f.readlines()
                f.close()

                self.vidFileName = allLines[0]
                self.vidFileName = self.vidFileName[:-1]
                allLines.remove(allLines[0])

                if len(allLines) == 0:
                    raise Exception('')

                # reset data for graphs
                self.data1 = []
                self.data2 = []
                self.timings = []
                self.emotions = []
                self.plot1.getAxis('bottom').setTicks([])
                self.plot2.getAxis('bottom').setTicks([])

                for line in allLines:
                    x = line.split('|')
                    self.data1.append(int(x[0]))
                    self.data2.append(int(x[1]))
                    self.timings.append(x[2])
                    self.emotions.append(x[3])

        except:
            self.fromFile = False

            # reset data for graphs
            self.data1 = []
            self.data2 = []
            self.timings = []
            self.emotions = []
            self.plot1.getAxis('bottom').setTicks([])
            self.plot2.getAxis('bottom').setTicks([])

            QMessageBox.about(self, "Ошибка!", "Выберите корректный файл!")
            return

    def loadSettings(self):

        path, _ = QFileDialog.getOpenFileName(self, "Открыть настройки",
                                                          QDir.homePath(), "txt files (*.txt)")
        if path != '':
            f = open(path, 'r')

            allLines = f.readlines()
            f.close()

            # считываем данные из файла и записываем эмоции
            self.emotions.clear()
            for line in allLines:
                s = line.rstrip("\r\n")
                x = s.split('|')
                emotion = Emotion(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]))
                self.emotions.append(emotion)
            self.settings.loadEmotions(self.emotions)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Настройки загружены из файла.")
            msg.setWindowTitle("Уведомление")
            msg.exec_()
            self.openSettings()
    

    def openSettings(self):
        self.settings.show()
    
class SettingsWindow(QtWidgets.QMainWindow, settingsdesign.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.emotions = []
        self.setWindowTitle("Настройки")
        # когда нажимаем на кнопку "добавить эмоцию"
        self.addButton.clicked.connect(self.addItem)
        
        # когда нажимаем на кнопку "удалить эмоцию"
        self.deleteButton.clicked.connect(self.deleteItem)
          
        # когда нажимаем на кнопку "сохранить настройки"
        self.saveButton.clicked.connect(self.saveSettings)

        # суем emotions[] в listView
        self.model = QtGui.QStandardItemModel()
        self.emotionsView.setModel(self.model)
        # for i in self.emotions:
        #     item = QtGui.QStandardItem(i.name)
        #     self.model.appendRow(item)

    def loadEmotions(self, _emotions):        
        self.emotions.clear()
        self.model.removeRows(0, self.model.rowCount())
        for emotion in _emotions:
            self.emotions.append(emotion)
            self.model.appendRow(QtGui.QStandardItem(emotion.name + ": " + str(emotion.from_strength) + "/" + str(emotion.to_strength) + "/" + str(emotion.from_color) + "/" + str(emotion.to_color)))

    def addItem(self):

        if self.emotionStrength1.text().isdigit() and self.emotionStrength2.text().isdigit() and self.emotionColor1.text().isdigit() and self.emotionColor2.text().isdigit() and int(self.emotionStrength1.text()) < int(self.emotionStrength2.text()) and int(self.emotionColor1.text()) < int(self.emotionColor2.text()):
            # создаем новую эмоцию из данных в лейблах
            emotion = Emotion(self.emotionName.text(), int(self.emotionStrength1.text()), int(self.emotionStrength2.text()), int(self.emotionColor1.text()), int(self.emotionColor2.text()))

            # записываем ее в листвью
            self.model.appendRow(QtGui.QStandardItem(emotion.name + ": " + str(emotion.from_strength) + "/" + str(emotion.to_strength) + "/" + str(emotion.from_color) + "/" + str(emotion.to_color)))

            # добавляем в экземпляр класса MindReaderApp
            self.emotions.append(emotion)

            # clear
            self.emotionName.setText("")
            self.emotionStrength1.setText("")
            self.emotionStrength2.setText("")
            self.emotionColor1.setText("")
            self.emotionColor2.setText("")
        else:
            # выводим ошибку в случае некорректности данных
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Введен некорректный диапазон.")
            msg.setWindowTitle("Ошибка!")
            msg.exec_()

    def deleteItem(self):
        selectedIndexes = self.emotionsView.selectedIndexes()
        selectedRows = [item.row() for item in selectedIndexes]
        modelTmp = self.emotionsView.model()
        for selectedRow in sorted(selectedRows, reverse = True):
            modelTmp.removeRow(selectedRow)
            del self.emotions[selectedRow]
            
    def saveSettings(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить данные",
                                                          QDir.homePath())
        if path != '':
            f = open(path, 'w+')
            for emotion in self.emotions:
                f.write(emotion.name + "|" + str(emotion.from_strength) + "|" + str(emotion.to_strength) + "|" + str(emotion.from_color) + "|" + str(emotion.to_color) + "\n")
            f.close()

class Emotion(object):
    
    name = ""
    from_strength = 0
    to_strength = 0
    from_color = 0
    to_color = 0

    def __init__(self, n, fs, ts, fc, tc):
        self.name = n
        self.from_strength = fs
        self.to_strength = ts
        self.from_color = fc
        self.to_color = tc
        
def main():

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MindReaderApp()  # Создаём объект класса MindReaderApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
