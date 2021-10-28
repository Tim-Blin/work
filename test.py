import csv
import numpy as np
from matplotlib import pyplot as plt

class deal:
    pass


def crop_to_opers(table):
    while(len(table[0]) == 0 or table[0][0] != 'Направление'):
        #print(table[0])
        table.pop(0)
    table.pop(0)
    return table

def read_table(file_name):
    table = []
    File = open(file_name, encoding='utf-8')
    reader = csv.reader(File, delimiter=';')
    for row in reader:
        table.append(row)
    File.close()
    return table

def integrated(x):
    s = 0
    for i in range(len(x)):
        s = s + x[i]
        x[i] = s
    return x

def d_acc_pos_free_3(table):
    start_index = min([int(i[2]) for i in table])
    end_index = max([int(i[3]) for i in table])
    length = end_index - start_index + 1
    acc = np.zeros(length)
    acc_b = np.zeros(length)
    acc_s = np.zeros(length)
    pos = np.zeros(length)
    pos_b = np.zeros(length)
    pos_s = np.zeros(length)
    free = np.zeros(length)
    free_b = np.zeros(length)
    free_s = np.zeros(length)
    for row in table:
        direct = row[0]
        close_type = row[1]
        entry_ind = int(row[2]) - start_index
        exit_ind = int(row[3]) - start_index
        entry_price = int(row[4])
        exit_price = int(row[5])
        if(direct == 'B'):
            acc_b[exit_ind] += exit_price - entry_price
            pos_b[entry_ind] += 1
            pos_b[exit_ind] -= 1
            free_b[entry_ind] -= entry_price
            free_b[exit_ind] += exit_price
            acc[exit_ind] += exit_price - entry_price
            pos[entry_ind] += 1
            pos[exit_ind] -= 1
            free[entry_ind] -= entry_price
            free[exit_ind] += exit_price
        elif(direct == 'S'):
            acc_s[exit_ind] -= exit_price - entry_price
            pos_s[entry_ind] -= 1
            pos_s[exit_ind] += 1
            free_s[entry_ind] += entry_price
            free_s[exit_ind] -= exit_price
            acc[exit_ind] -= exit_price - entry_price
            pos[entry_ind] -= 1
            pos[exit_ind] += 1
            free[entry_ind] += entry_price
            free[exit_ind] -= exit_price
        else: raise ValueError('operation is nither B or S')
    return [[acc, pos, free], 
            [acc_b, pos_b, free_b],
            [acc_s, pos_s, free_s]]

def acc_pos_free_3(table):
    counts = d_acc_pos_free_3(table)
    return [[integrated(x) for x in y] for y in counts]

def d_acc(table, start_index, end_index):
    length = end_index - start_index + 1
    acc = np.zeros(length)
    for row in table:
        direct = row[0]
        entry_ind = int(row[2]) - start_index
        exit_ind = int(row[3]) - start_index
        entry_price = int(row[4])
        exit_price = int(row[5])
        if(direct == 'B'):
            acc[exit_ind] += exit_price - entry_price
        elif(direct == 'S'):
            acc[exit_ind] -= exit_price - entry_price
        else: raise ValueError('operation is nither B or S')

filename = 'D:\work\programming\mathclub\example.csv'
counts = acc_pos_free_3(crop_to_opers(read_table(filename)))

#plt.plot(counts[1][0])
#plt.plot(counts[1][1])
plt.plot(counts[0][1])
#plt.plot(counts[2][1])

plt.show()

for i in range(3):
    for j in range(3):
        plt.plot(counts[i][j])
        print(i, j)
        plt.show()
