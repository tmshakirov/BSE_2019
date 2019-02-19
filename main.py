import random
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import design  # Это наш конвертированный файл дизайна
import pyqtgraph as pg
import numpy as np

class MindReaderApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.startButton.clicked.connect(lambda: self.start_timer(10, 10))

        # настраиваем график
        self.timer = QtCore.QTimer()
        self.win = pg.GraphicsWindow()
        self.p3 = self.win.addPlot()
        self.curve3 = self.p3.plot()
        self.setGraph()

        self.data3 = np.empty(100)
        self.ptr3 = 0

        # запускает таймер, который работает заданное количество секунд
        self.clicked = False
    def start_timer(self, seconds=10, interval=10):

        if(self.clicked):
            self.startButton.setText("Запустить")
            self.timer.stop()
            self.clicked = False
        else:
            self.startButton.setText("Остановить")
            counter = 0
            count = seconds * 1000 / interval

            self.data3 = np.empty(100)
            self.ptr3 = 0

            def handler():
                nonlocal counter
                counter += 1
                self.update(counter)
                #if counter >= count:
                    #self.timer.stop()
                    #self.timer.deleteLater()

            self.timer.timeout.connect(handler)
            self.timer.start(interval)
            self.clicked = True

    # то что происходит каждый тик таймера
    def update(self, counter):
        #заглушка для считываемого потока
        x = random.randint(0, 100)


        self.EmotionLabel.setText(str(counter))
        self.updateGraph(x)

    def setGraph(self):
        self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        # Use automatic downsampling and clipping to reduce the drawing load
        self.p3.setDownsampling(mode='peak')
        self.p3.setClipToView(True)
        self.p3.setRange(xRange=[-100, 0])
        self.p3.setLimits(xMax=0)


    def updateGraph(self, x):
        self.data3[self.ptr3] = x
        self.ptr3 += 1
        # increase arr of data
        if self.ptr3 >= self.data3.shape[0]:
            tmp = self.data3
            self.data3 = np.empty(self.data3.shape[0] * 2)
            self.data3[:tmp.shape[0]] = tmp

        self.curve3.setData(self.data3[:self.ptr3])
        self.curve3.setPos(-self.ptr3, 0)



def main():
    import pyqtgraph.examples
    pyqtgraph.examples.run()

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MindReaderApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()