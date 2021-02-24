import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView

import design  # Это наш конвертированный файл дизайна
import numpy as np
import random


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        def open(self):

            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            fileName = filename[0]

            w_l = 1
            random.seed(20)
            arr = np.loadtxt(fileName)
            self.arr = arr
            length = np.shape(arr)
            w_list = np.full(length[1], w_l)
            p_e = np.zeros(length[0])
            N_iter = 10000

            for i in range(length[0]):
                p_e[i] = np.sum(arr[i] * w_l) / np.sum(w_list)

            self.p_e = p_e

            arr_PV = np.zeros((length[0], length[0]))

            for i in range(length[0]):
                for j in range(length[0]):
                    if i != j:
                        left_lim = max(0, (p_e[i] - 1 + p_e[j]) / p_e[j])
                        right_lim = min(1, p_e[i] / p_e[j])
                        arr_PV[i][j] = random.uniform(left_lim, right_lim)
            self.arr_PV = arr_PV
            arr_PV_res = np.column_stack((p_e, arr_PV))

            p_e_ch = p_e / (1 - p_e)
            self.p_e_ch = p_e_ch
            arr_chance = arr_PV / (1 - arr_PV)
            self.arr_chance = arr_chance
            arr_ch_res = np.column_stack((p_e_ch, arr_chance))

            arr_rel = arr_chance / p_e_ch
            self.arr_rel = arr_rel
            arr_rel_res = np.column_stack((p_e_ch, arr_rel))

            num_scen = 0
            arr_scen = np.zeros((length[0], length[0]))

            for i in range(0, length[0]):
                arr_scen[i] = arr_PV[:, i]

            for k in range(0, length[0]):

                N_count = np.zeros(length[0])

                for i in range(0, N_iter):
                    for j in range(0, length[0]):
                        if arr_scen[k][j] < random.uniform(0, 1):
                            N_count[j] += 1

                for i in range(0, length[0]):
                    if i == k:
                        arr_scen[k][i] = 1
                    else:
                        arr_scen[k][i] = N_count[i] / N_iter

            showArr("vector_widget", "Подія", "P", self.p_e)
            showArr("arr_widget", "Експерт", "Подія", self.arr)

            self.rdBtnArr.setChecked(True)
            self.rdBtnPe.setChecked(True)




        self.fileBtn.clicked.connect(lambda: open(self))



        def insertDataTable(table, arr):
            if len(np.shape(arr)) > 1:
                row = np.shape(arr)[0]
                column = np.shape(arr)[1]
            else:
                row = 1
                column = np.shape(arr)[0]

            for i in range(row):
                for j in range(column):
                    if len(np.shape(arr)) > 1:
                        getattr(self, table).setItem(i, j, QtWidgets.QTableWidgetItem("%.4f" % (arr[i, j])))
                    else:
                        getattr(self, table).setItem(i, j, QtWidgets.QTableWidgetItem("%.4f" % (arr[j])))
            getattr(self, table).resizeColumnsToContents()
            getattr(self, table).horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def setTableLabels(table, col_name, row_name, arr):
            if len(np.shape(arr)) > 1:
                row = np.shape(arr)[0]
                column = np.shape(arr)[1]
            else:
                row = 1
                column = np.shape(arr)[0]

            getattr(self, table).setColumnCount(column)
            getattr(self, table).setRowCount(row)
            cols_name = []
            rows_name = []

            if column > 1:
                [cols_name.append(col_name + str(i + 1)) for i in range(column)]
            else:
                cols_name.append(col_name)

            if row > 1:
                [rows_name.append(row_name + str(i + 1)) for i in range(row)]
            else:
                rows_name.append(row_name)

            getattr(self, table).setHorizontalHeaderLabels(cols_name)
            getattr(self, table).setVerticalHeaderLabels(rows_name)

        def showArr(table, col_name, row_name, arr):

            setTableLabels(table, col_name, row_name, arr)
            insertDataTable(table, arr)

        self.rdBtnArr.clicked.connect(lambda: showArr("arr_widget","Експерт", "Подія", self.arr))
        self.rdBtnArrPV.clicked.connect(lambda: showArr("arr_widget","Подія", "Подія", self.arr_PV))
        self.rdBtnArrChance.clicked.connect(lambda: showArr("arr_widget","Подія", "Подія", self.arr_chance))
        self.rdBtnArrRel.clicked.connect(lambda: showArr("arr_widget","Подія", "Подія", self.arr_rel))
        self.rdBtnPe.clicked.connect(lambda: showArr("vector_widget","Подія", "P", self.p_e))
        self.rdBtnPeChance.clicked.connect(lambda: showArr("vector_widget","Подія", "P", self.p_e_ch))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
