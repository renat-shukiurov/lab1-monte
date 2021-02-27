import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView

import design  # Это наш конвертированный файл дизайна
import design2  # Это наш конвертированный файл дизайна
import numpy as np
import random
import math



class FirstWindow(QtWidgets.QMainWindow, design.Ui_MethodPV_Radio):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.w = None  # No external window yet.
        self.setWindowTitle("MethodPV_Radio")

        def pv_method(self):

            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', "", "TXT files (*.txt)")
            fileName = filename[0]
            #fileName = "data.txt"
            w_l = 1
            random.seed(20)
            arr = np.loadtxt(fileName)
            self.arr = arr
            length = np.shape(arr)
            self.length = length
            w_list = np.full(length[1], w_l)
            p_e = np.zeros(length[0])
            N_iter = 10000
            self.N_iter = N_iter

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

            self.arr_scen = arr_scen

            showArr("vector_widget", "Подія", "P", self.p_e)
            showArr("arr_widget", "Експерт", "Подія", self.arr)

            self.rdBtnArr.setCheckable(True)
            self.rdBtnArrPV.setCheckable(True)
            self.rdBtnArrChance.setCheckable(True)
            self.rdBtnArrRel.setCheckable(True)
            self.rdBtnPe.setCheckable(True)
            self.rdBtnPeChance.setCheckable(True)

            self.rdBtnArr.clicked.connect(lambda: showArr("arr_widget", "Експерт", "Подія", self.arr))
            self.rdBtnArrPV.clicked.connect(lambda: showArr("arr_widget", "Подія", "Подія", self.arr_PV))
            self.rdBtnArrChance.clicked.connect(lambda: showArr("arr_widget", "Подія", "Подія", self.arr_chance))
            self.rdBtnArrRel.clicked.connect(lambda: showArr("arr_widget", "Подія", "Подія", self.arr_rel))
            self.rdBtnPe.clicked.connect(lambda: showArr("vector_widget", "Подія", "P", self.p_e))
            self.rdBtnPeChance.clicked.connect(lambda: showArr("vector_widget", "Подія", "P", self.p_e_ch))

            self.rdBtnArr.setChecked(True)
            self.rdBtnPe.setChecked(True)

            self.openWindow.clicked.connect(lambda: showSecondWindow(self))

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

            rows_name = []

            if type(col_name) is str:
                cols_name = []

                if column > 1:
                    [cols_name.append(col_name + str(i + 1)) for i in range(column)]
                else:
                    cols_name.append(col_name)
            else:
                cols_name = col_name

            if row > 1:
                [rows_name.append(row_name + str(i + 1)) for i in range(row)]
            else:
                rows_name.append(row_name)

            getattr(self, table).setHorizontalHeaderLabels(cols_name)
            getattr(self, table).setVerticalHeaderLabels(rows_name)

        def showArr(table, col_name, row_name, arr):

            setTableLabels(table, col_name, row_name, arr)
            insertDataTable(table, arr)

        def showSecondWindow(self):
            if self.w is None:
                self.w = SecondWindow(self)
            self.w.show()

        self.fileBtn.clicked.connect(lambda: pv_method(self))
        self.exitBtn.clicked.connect(self.close)



class SecondWindow(QtWidgets.QWidget, design2.Ui_Scenaries):
    def __init__(self, bigSelf):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("MonteScenaries_Radio")
        self.arr = bigSelf.arr
        self.arr_PV = bigSelf.arr_PV
        self.p_e = bigSelf.p_e
        self.arr_scen = bigSelf.arr_scen
        self.length = bigSelf.length
        self.N_iter = bigSelf.N_iter

        def insertDataTable(table, arr):
            if len(np.shape(arr)) > 1:
                row = np.shape(arr)[0]
                column = np.shape(arr)[1]
            elif table == "t_sigma":
                column = 1
                row = np.shape(arr)[0]
            else:
                row = 1
                column = np.shape(arr)[0]


            for i in range(row):
                for j in range(column):
                    if len(np.shape(arr)) > 1:
                        getattr(self, table).setItem(i, j, QtWidgets.QTableWidgetItem("%.4f" % (arr[i, j])))
                    elif table == "t_sigma":
                        getattr(self, table).setItem(i, j, QtWidgets.QTableWidgetItem("%.4f" % (arr[i])))
                    else:
                        getattr(self, table).setItem(i, j, QtWidgets.QTableWidgetItem("%.4f" % (arr[j])))
            if table == "t_sigma":
                getattr(self, table).resizeColumnsToContents()
            getattr(self, table).verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def setTableLabels(table, col_name, row_name, arr):
            if len(np.shape(arr)) > 1:
                row = np.shape(arr)[0]
                column = np.shape(arr)[1]
            elif table == "t_sigma":
                column = 1
                row = np.shape(arr)[0]
            else:
                row = 1
                column = np.shape(arr)[0]

            getattr(self, table).setColumnCount(column)
            getattr(self, table).setRowCount(row)

            rows_name = []

            if type(col_name) is str:
                cols_name = []

                if column > 1:
                    [cols_name.append(col_name + str(i + 1)) for i in range(column)]
                else:
                    cols_name.append(col_name)
            else:
                cols_name = col_name

            if row > 1:
                [rows_name.append(row_name + str(i + 1)) for i in range(row)]
            else:
                rows_name.append(row_name)

            getattr(self, table).setHorizontalHeaderLabels(cols_name)
            getattr(self, table).setVerticalHeaderLabels(rows_name)

        def showArr(table, col_name, row_name, arr):

            setTableLabels(table, col_name, row_name, arr)
            insertDataTable(table, arr)

        def getScenario(n, d):

            p_test = self.p_e.copy()
            p_test[n] = 1
            d.append(list(self.arr_scen[i] - p_test))
            res_scen = np.vstack(np.column_stack((self.p_e, p_test, self.arr_scen[n], self.arr_scen[n] - p_test)))

            return res_scen

        self.delta_list = []

        for i in range(np.shape(self.arr)[0]):
            showArr("t" + str(i + 1), ["Початкова", "Тестова", "Фінальна", "Різниця"], "Подія", getScenario(i, self.delta_list))

        self.res_delta = np.array(self.delta_list) ** 2

        sigma = np.zeros(self.length[0])
        for i in range(self.length[0]):
            sum_1, sum_2 = 0, 0
            for j in range(self.length[1]):
                sum_1 += math.pow(self.arr[i][j], 2)
                sum_2 += self.arr[i][j]
            sigma[i] = math.sqrt((self.length[1] * sum_1 - math.pow(sum_2, 2)) / (self.length[1] * (self.length[1] - 1)))

        showArr("t_sigma", ["Sigma"], "", sigma)

        max_delta = []

        for i in range(len(self.res_delta[0])):
            max_delta.append(np.max(self.res_delta[i]))

        max_delta = np.array(max_delta)

        L1 = np.sum(max_delta) / self.length[0] / 2
        L4 = 3 / math.sqrt(self.N_iter)
        IKD = (1 - L1) * (1 - L4)

        self.l1.setText("%.2f" % (L1))
        self.l4.setText(str(L4))
        self.IKD.setText("%.2f" % (IKD) + " ~ " + str(int(IKD * 100)) + "%")
        self.exitBtn.clicked.connect(self.close)






def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = FirstWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
