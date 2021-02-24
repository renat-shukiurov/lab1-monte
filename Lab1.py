import numpy as np
import random
import math
import design
import sys

w_l = 1
random.seed(20)
arr = np.loadtxt('data2.txt')
length = np.shape(arr)
w_list = np.full(length[1], w_l)
p_e = np.zeros(length[0])
N_iter = 10000

for i in range(length[0]):
    p_e[i] = np.sum(arr[i]*w_l)/np.sum(w_list)

arr_PV = np.zeros((length[0], length[0]))

for i in range(length[0]):
    for j in range(length[0]):
        if i != j:
            left_lim = max(0, (p_e[i] - 1 + p_e[j])/p_e[j])
            right_lim = min(1, p_e[i]/p_e[j])
            arr_PV[i][j] = random.uniform(left_lim, right_lim)
arr_PV_res = np.column_stack((p_e, arr_PV))


p_e_ch = p_e/(1 - p_e)
arr_chance = arr_PV/(1 - arr_PV)
arr_ch_res = np.column_stack((p_e_ch, arr_chance))

arr_rel = arr_chance/p_e_ch
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
            arr_scen[k][i] = N_count[i]/N_iter

sigma = np.zeros(length[0])
for i in range(length[0]):
    sum_1, sum_2 = 0, 0
    for j in range(length[1]):
        sum_1 += math.pow(arr[i][j], 2)
        sum_2 += arr[i][j]
    sigma[i] = math.sqrt((length[1] * sum_1 - math.pow(sum_2, 2))/(length[1]*(length[1] - 1)))

for i in range(length[0]):
    p_test = p_e.copy()
    p_test[i] = 1
    res_scen = np.vstack(np.column_stack((p_e, p_test, arr_scen[i], arr_scen[i] - p_test)))
print(res_scen)


