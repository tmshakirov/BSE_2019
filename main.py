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

        # настраиваем графики
        self.timer = QtCore.QTimer()

        self.plot1 = self.graphic1.addPlot()
        self.curve1 = self.plot1.plot()

        self.plot2 = self.graphic2.addPlot()
        self.curve2 = self.plot2.plot()
        self.setGraphs()

        # задаем массивы для хранения данных
        self.data1 = np.empty(100)
        self.data2 = np.empty(100)
        self.ptr1 = 0
        self.ptr2 = 0

        # запускает таймер, который работает заданное количество секунд
        self.clicked = False

    def start_timer(self, seconds=10, interval=10):

        if(self.clicked):
            self.startButton.setText("Запустить")
            self.timer.stop()
            self.clicked = False

            # reset data for graphs
            self.data1 = np.empty(100)
            self.data2 = np.empty(100)
            self.ptr1 = 0
            self.ptr2 = 0
        else:
            self.startButton.setText("Остановить")
            counter = 0
            count = seconds * 1000 / interval

            self.data1 = np.empty(100)
            self.ptr1 = 0

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
        y = random.randint(0, 100)


        self.EmotionLabel.setText(str(counter))
        self.updateGraphs(x, y)

    def setGraphs(self):
        # self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        # Use automatic downsampling and clipping to reduce the drawing load
        self.plot1.setDownsampling(mode='peak')
        self.plot1.setClipToView(True)
        self.plot1.setRange(xRange=[-100, 0])
        self.plot1.setLimits(xMax=0)

        self.plot2.setDownsampling(mode='peak')
        self.plot2.setClipToView(True)
        self.plot2.setRange(xRange=[-100, 0])
        self.plot2.setLimits(xMax=0)

    def updateGraphs(self, x, y):
        # increase first graph
        self.data1[self.ptr1] = x
        self.ptr1 += 1
        # increase arr of data1
        if self.ptr1 >= self.data1.shape[0]:
            tmp = self.data1
            self.data1 = np.empty(self.data1.shape[0] * 2)
            self.data1[:tmp.shape[0]] = tmp

        self.curve1.setData(self.data1[:self.ptr1])
        self.curve1.setPos(-self.ptr1, 0)

        # increase second graph
        self.data2[self.ptr2] = y
        self.ptr2 += 1
        # increase arr of data2
        if self.ptr2 >= self.data2.shape[0]:
            tmp = self.data2
            self.data2 = np.empty(self.data2.shape[0] * 2)
            self.data2[:tmp.shape[0]] = tmp

        self.curve2.setData(self.data2[:self.ptr2])
        self.curve2.setPos(-self.ptr2, 0)



def main():
    import pyqtgraph.examples
    pyqtgraph.examples.run()

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MindReaderApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()