import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
import numpy as np
import random

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        arr = np.loadtxt('data.txt')
        length = np.shape(arr)

        self.arr_widget.setColumnCount(length[1])
        self.arr_widget.setRowCount(length[0])

        for i in range(length[0]):
            for j in range(length[1]):
                self.arr_widget.setItem(i,j,QtWidgets.QTableWidgetItem(str(arr[i,j])))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()