import os
import random
import sys  # sys нужен для передачи argv в QApplication
import numpy as np
import cv2
import serial
import glob
import time
from scipy.signal import butter, lfilter
from numpy.fft import rfft
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QAction, QWidget
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
        

        self.timer = None
        self.time = QtCore.QTime(0, 0, 0)

        self.maxTimer = 0.0

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
        self.qw = QWidget()
        self.qw.setGeometry(10, 360, 611, 280)
        self.qw.setParent(self)
        self.faceVideoWidget = QVideoWidget()
        self.faceVideoWidget.setParent(self.qw)
        self.faceVideoWidget.show()
        self.facePlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.facePlayer.setVideoOutput(self.faceVideoWidget)
        self.facePlayer.durationChanged.connect(self.getDuration)
        self.chooseVideo.triggered.connect(self.openFile)
        self.videoChosed = False

        # для записи лица
        self.videoTimer = None
        self.frame = None
        self.capture = None
        self.fps = int(30)
        self.videoSaver = None
        if not os.path.exists('Recordings'):
            os.makedirs('Recordings')    

        # настройка порта
        self.ser = serial.Serial()
        self.ser.baudrate = 57600
        self.port = ""
        self.choosePort.triggered.connect(self.inputCom)

        # файл
        if not os.path.exists('Sessions'):
            os.makedirs('Sessions')    
        self.vidFileName = ""
        self.faceFileName = ""

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
        self.pause_video()
        self.mediaPlayer.stop()
        self.facePlayer.stop()
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
            if self.fromFile:
                try:
                    self.faceWidget.hide()
                    self.facePlayer.setMedia(
                        QMediaContent(QUrl.fromLocalFile(self.faceFileName)))
                    self.qw.show()
                    self.facePlayer.play()
                    self.start = time.time()
                except Exception as e:
                    QMessageBox.about(self, "Ошибка!", "Видеофайл отсутствует или поврежден.")
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

                self.qw.hide()
                self.faceWidget.show()

                self.set_camera(self.frame)

                # reset data for graphs
                self.data1 = []
                self.data2 = []
                self.timings = []
                self.emotions = []
                self.plot1.getAxis('bottom').setTicks([])
                self.plot2.getAxis('bottom').setTicks([])

                # new file
                self.fname = str(len([name for name in os.listdir('Sessions') if os.path.isfile(os.path.join('Sessions', name))])) + '.emtn'
                if not os.path.isfile('Sessions/' + self.fname):
                    self.f = open('Sessions/' + self.fname, 'w')
                    self.f.close()
                self.f = open('Sessions/' + self.fname, 'r')
                self.f = open('Sessions/' + self.fname, 'w')
                self.f.write(self.vidFileName + "\n")
                self.f.write(os.getcwd() + '/Recordings/{}.avi'.format(self.faceFileName) + "\n")
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
    
    def set_camera(self, frame):
        try:
            if not self.fromFile:
                self.capture = cv2.VideoCapture(0)
                self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.fps = self.capture.get(cv2.CAP_PROP_FPS)
                if self.fps == 0 or self.fps == -1:
                    self.fps = int(25)
                    print("Warning: OpenCV failed to get your camera's frame rate, set to {}.".format(self.fps))
                # start                
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.faceFileName = len([name for name in os.listdir('Recordings') if os.path.isfile(os.path.join('Recordings', name))])
                self.videoSaver = cv2.VideoWriter('Recordings/{}.avi'.format(self.faceFileName),fourcc, cv2.CAP_PROP_FPS, (int(self.width), int(self.height)))
                self.start_video()

        except Exception as e:
                self.capture = None
                QMessageBox.about(self, "Ошибка!", "Невозможно использовать вашу камеру.")
                print(str(e))
 
    
    def _draw_frame(self, frame):
        # convert to pixel
        cvtFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(cvtFrame, self.width, self.height, QImage.Format_RGB888)
        pix = QPixmap.fromImage(img) 
        self.faceWidget.setPixmap(pix)   
        outFrame = cv2.cvtColor(cvtFrame, cv2.COLOR_BGR2RGB) 
        self.videoSaver.write(outFrame)
        QtGui.QApplication.processEvents()

    def _next_frame(self):
        try:
            if self.capture is not None:
                _ret, frame = self.capture.read()
                if frame is None:
                    QMessageBox.about(self, "Ошибка!", "Ошибка считывания изображения.")
                    print("ERROR: Read next frame failed with returned value {}.".format(_ret)) 
 
                # Draw.
                self._draw_frame(frame)
 
        except Exception as e:
            QMessageBox.about(self, "Ошибка!", "Ошибка считывания изображения.")
            print(str(e))
            # Saving output video
            if self.videoSaver:
                self.videoSaver.release()
           
    def start_video(self):
            self.videoTimer = QtCore.QTimer()
            self.videoTimer.timeout.connect(self._next_frame)
            self.videoTimer.start(1000 // self.fps)
        
    def pause_video(self):
        try:
            if self.capture != None:
                self.capture.release()
            self.capture = None
            self.faceWidget.clear()
            self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            self.mediaPlayer.setVideoOutput(self.videoWidget)
            self.qw.show()
            self.faceWidget.show()
            self.videoSaver = None
            cv2.destroyAllWindows()
            self.clicked = False
            print("INFO: Streaming paused.")
        except Exception as e:
            print(str(e))

    def getDuration(self):
        self.maxTimer = float(self.facePlayer.duration()/1000)   
        print(self.maxTimer)    

    # то что происходит каждый тик таймера
    def update(self):

        self.counter += 1
        # заглушка для считываемого потока
        # x = random.randint(0, 100)
        # y = random.randint(0, 100)
        ########################

        if not self.fromFile:
            # считка с устройства
            ch1, ch2 = self.readFromEEG()

            # получаем эмоцию
            emtn = self.getEmotion(ch1, ch2)

        # точки выводятся каждые 100 мс
        interval = 100 / 4
        if not self.fromFile:
            interval = 0.1 / 4
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
            if (self.counter1 < len(self.data1)):
                self.EmotionLabel.setText("Текущая эмоция: " + self.emotions[self.counter1])
                self.updateGraphs()
                self.counter1 += 1
            curTime = time.time()
            # если все данные уже показаны то стоп
            if self.fromFile and (curTime-self.start) > self.maxTimer and self.counter1 >= len(self.data1):
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
                    QDir.homePath(), "video files (*.avi *.mp4 *.gif)")

            if self.vidFileName != '':
                self.videoChosed = True

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a
 
    def butter_bandpass_filter(self, data, lowcut, highcut, fs=256, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y
 
    def filter(self, data, hi, lo):
        fs = np.fft.rfft(data)
        q = np.fft.rfftfreq(len(data), 256)
 
        fs[(q>hi)] = 0
        fs[(q<lo)] = 0
        return np.fft.irfft(fs)
 
    def readFromEEG(self):
        n = 26
        strArr = np.zeros(n)
        pArr = np.zeros(n)
 
        for i in range(0, n):
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
            strArr[i] = ch1
            # 7 and 8
            ch2 = conv2sig(self.ser.read(), self.ser.read())
            pArr[i] = ch2
 
        out1 = self.butter_bandpass_filter(strArr, 8, 12)
        out2 = self.butter_bandpass_filter(pArr, 12, 30)
        # out1 = self.filter(strArr, 8, 12)
        # out2 = self.butter_bandpass_filter(strArr, 8, 12)
 
        a1 = np.mean(out1)
        a2 = abs(out1.min()) + abs(out1.max())
        a3 = out1[len(out1) - 1]
 
        b1 = np.mean(out2)
        b2 = out2.min()
        b3 = out2[len(out2) - 1]
 
        return a2, b2

    def inputCom(self):

        text, ok = QInputDialog.getText(self, 'Выбор COM порта', 'Введите номер COM порта, к которому подключено устройство:')

        if ok:
            if sys.platform.startswith('win'):
                self.port = 'COM' + text
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                self.port = '/dev/ttyUSB' + text
            elif sys.platform.startswith('darwin'):
                self.port = '/dev/ttyUSB' + text
            else:
                raise EnvironmentError('Unsupported platform')
            self.ser.port = self.port
            if not self.ser.isOpen():
                try:
                    self.ser.open()
                except serial.SerialException:
                    QMessageBox.about(self, "Ошибка!", "Выберите работающий COM порт!")

    def loadFile(self):

        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл",
                                                          QDir.homePath(), "Emotion Files (*.emtn)")
        if path != '':
            self.fromFile = True
            f = open(path, 'r', encoding='utf-8', errors='ignore')

            allLines = f.readlines()
            f.close()
            try:
                self.vidFileName = allLines[0]
                self.vidFileName = self.vidFileName[:-1]
                
                self.faceFileName = allLines[1]
                self.faceFileName = self.faceFileName[:-1]
                allLines.remove(allLines[0])
                allLines.remove(allLines[0])

                # reset data for graphse
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

            except Exception as e:
                QMessageBox.about(self, "Ошибка!", "Файл поврежден или неверно сформирован.")
                

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
    window.showMaximized()  # Показываем окно
    window.setFixedSize(app.desktop().screenGeometry().width(), app.desktop().screenGeometry().height())
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
