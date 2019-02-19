import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import design  # Это наш конвертированный файл дизайна


class MindReaderApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    timer = QtCore.QTimer()

    # запускает таймер, который работает заданное количество секунд
    def start_timer(self, seconds=10, interval=10):
        counter = 0
        count = seconds * 1000 / interval

        def handler():
            nonlocal counter
            counter += 1
            self.update(counter)
            if counter >= count:
                self.timer.stop()
                self.timer.deleteLater()

        self.timer.timeout.connect(handler)
        self.timer.start(interval)

    # то что происходит каждый тик таймера
    def update(self, counter):
        self.EmotionLabel.setText(str(counter))

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.startButton.clicked.connect(lambda: self.start_timer(10, 10))





def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MindReaderApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()