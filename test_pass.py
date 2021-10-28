import csv
import numpy as np
from matplotlib import pyplot as plt
import config

class deal:
    def __init__(self, row):
        self.direct = row[0]
        self.close_type = row[1]
        self.entry_ind = int(row[2])
        self.exit_ind = int(row[3])
        self.entry_price = int(row[4])
        self.exit_price = int(row[5])

def read_table(file_name):
    File = open(file_name, encoding='utf-8')
    reader = csv.reader(File, delimiter=';')
    table = []
    nex = reader.__next__()
    while len(nex) == 0 or nex[0] != 'Направление':
        nex = reader.__next__()
    for row in reader:
        table.append(deal(row))
    File.close()
    return table

class history:
    def __init__(self, table):
        self.table = table
        self.move_table_indexes_to_zero()

    def move_table_indexes_to_zero(self):
        self.start_index = min([row.entry_ind for row in self.table]) + 1
        for row_ind in range(len(self.table)):
            self.table[row_ind].entry_ind -= self.start_index
            self.table[row_ind].exit_ind -= self.start_index
        return self.table

    def find_end_index(self):
        self.end_index = max([row.exit_ind for row in self.table])
        return self.end_index

    def build_hystory(self, h_type, direct = None):
        try:
            end_index = self.end_index
        except:
            end_index = self.find_end_index()
        entry_d = {}
        exit_d = {}
        if h_type == 'acc':
            entry_d['B'] = lambda row: 0
            entry_d['S'] = lambda row: 0
            exit_d['B'] = lambda row: row.exit_price - row.entry_price
            exit_d['S'] = lambda row: row.entry_price - row.exit_price
        elif h_type == 'pos':
            entry_d['B'] = lambda row: 1
            entry_d['S'] = lambda row: -1
            exit_d['B'] = lambda row: -1
            exit_d['S'] = lambda row: 1
        elif h_type == 'free':
            entry_d['B'] = lambda row: -row.entry_price
            entry_d['S'] = lambda row: row.entry_price
            exit_d['B'] = lambda row: row.exit_price
            exit_d['S'] = lambda row: -row.exit_price
        else:
            raise ValueError('h_type can only be acc, pos or free')
        if direct == None:
            pass
        elif direct == 'B':
            entry_d['S'] = lambda row: 0
            exit_d['S'] = lambda row: 0
        elif direct == 'S':
            entry_d['B'] = lambda row: 0
            exit_d['B'] = lambda row: 0
        else:
            raise ValueError('direct can only be \'S\', \'B\' or None')
        hyst = np.zeros(end_index + 1)
        for row in self.table:
            hyst[row.entry_ind] += entry_d[row.direct](row)
            hyst[row.exit_ind] += exit_d[row.direct](row)
        hyst = integrated(hyst)
        if(h_type == 'acc'):
            self.d_acc = hyst
        elif(h_type == 'pos'):
            self.d_pos = hyst
        else:
            self.d_free = hyst
        return hyst

def integrated(x):
    s = 0
    for i in range(len(x)):
        s = s + x[i]
        x[i] = s
    return x

h = history(read_table(config.file_path + config.file_name))

for t in ['acc', 'pos', 'free']:
    for d in [None, 'B', 'S']:
        plt.plot(h.build_hystory(t, d))
#plt.plot(h.build_hystory('pos', 'S'))
plt.show()