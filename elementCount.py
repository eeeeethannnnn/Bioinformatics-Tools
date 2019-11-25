#!/usr/bin/env python
# Shebang line here
# Your code here
import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input1', type = str, default = sys.stdin, required = True)
args  = parser.parse_args()
fileName = args.input1

matrix = []
with open(fileName, 'r') as r:
    readFile = r.read()
    line = readFile.split('\n')
    for i in line:
        if i == '':
            continue
        else:
            matrix.append(i.split('\t'))
i = 1
count = 1
chr = ''
while i < len(matrix):
    if matrix[i][0] == matrix[i-1][0]: #same chr
        chr = matrix[i][0]
        if matrix[i][1] > matrix[i-1][1] and matrix[i][1] > matrix[i-1][2]: #no overlap
            print('{0}\t{1}\t{2}\t{3}\n'.format(matrix[i-1][0], matrix[i-1][1], matrix[i-1][2], count), end='')
            i += 1
        else : # overlap
            overlap = []
            while i < len(matrix) and matrix[i][1] < matrix[i-1][2]: #overlap not over
                tmp = []
                if int(matrix[i-1][2]) - int(matrix[i-1][1]) > 10000:
                    continue
                else:
                    tmp.append(int(matrix[i-1][1]))
                    tmp.append(int(matrix[i-1][2]))
                    overlap.append(tmp)
                i += 1
            tmp = []
            tmp.append(int(matrix[i-1][1]))
            tmp.append(int(matrix[i-1][2]))
            overlap.append(tmp)
            arr = []
            l = len(overlap)
            dif = overlap[l-1][1] - overlap[0][0]
            start = overlap[0][0]
            for j in range(dif):
                arr.append(0)
            for j in range(l):
                overlap[j][0] -= start
                overlap[j][1] -= start
            for j in range(l):
                for k in range(overlap[j][1] - overlap[j][0]):
                    arr[k+overlap[j][0]] += 1
            j = 1
            store = []
            while j < dif:
                if arr[j] != arr[j-1]:
                    tmp = []
                    tmp.append(j)
                    tmp.append(arr[j-1])
                    store.append(tmp)
                j += 1
            tmp = []
            tmp.append(len(arr))
            tmp.append(arr[-1])
            store.append(tmp)
            print('{0}\t{1}\t{2}\t{3}\n'.format(chr, start, store[0][0]+start, store[0][1]), end='')
            for j in range(len(store)-1):
                print('{0}\t{1}\t{2}\t{3}\n'.format(chr, start+store[j][0], start+store[j+1][0], store[j+1][1]), end='')
            i += 1
    else:
        print('{0}\t{1}\t{2}\t1\n'.format(matrix[i-1][0], matrix[i-1][1], matrix[i-1][2]), end='')
        i += 1
