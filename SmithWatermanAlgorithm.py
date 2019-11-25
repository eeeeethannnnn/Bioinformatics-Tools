#!/usr/bin/env python3
# Write your code here
import sys

sequence1 = ''
sequence2 = ''

# read fasta
with open(sys.argv[1], 'r') as seq1, open(sys.argv[2], 'r') as seq2:
    for line in seq1:
        if line.startswith('>'):
            continue
        else:
            sequence1 = line.strip('\n')
    for line in seq2:
        if line.startswith('>'):
            continue
        else:
            sequence2 = line.strip('\n')
#print(sequence1)
#ATCG
#print(sequence2)
#AACG
##### make the shorter sequence to be sequence1 #####
swap = False
if len(sequence2) < len(sequence1):
    sequence1, sequence2 = sequence2, sequence1
    swap = True
# initialize matrix
w, h = len(sequence1), len(sequence2)
#print(w)
#print(h)
matrix = [[0 for x in range(w + 1)] for y in range(h + 1)]
#for i in range(w+1):
#    matrix[0][i] = 0 - i
#for i in range(h+1):
#    matrix[i][0] = 0 - i

# biuld matrix
maximum = matrix[0][0]
max_x = 0
max_y = 0
for i in range(1, h + 1):
    for j in range(1, w + 1):
        if sequence2[i - 1] == sequence1[j - 1]: # sequence match
            diagonal = matrix[i - 1][j - 1] + 1 # match= +1
        else: # sequence mismatch
            diagonal = matrix[i - 1][j - 1] - 1 # mismatch = -1
        up = matrix[i - 1][j] - 1 # gap = -1
        left = matrix[i][j - 1] - 1 # gap = -1
        if max(diagonal, up, left) < 0:
            matrix[i][j] = 0
        else:
            matrix[i][j] = max(diagonal, up, left)
            if matrix[i][j] >= maximum:
                maximum = matrix[i][j]
                max_x = i
                max_y = j
#for i in range(len(matrix)):
#    for j in range(len(matrix[i])):
#        if j != len(matrix[i]) - 1:
#            print('{:>3}'.format(matrix[i][j]), end="")
#        else:
#            print('{:>3}'.format(matrix[i][j]))
#print(max_x, max_y, maximum)

# find backTrack
backTrack = []
h = max_x
w = max_y
end_x = 0
end_y = 0
while h != 0 and w != 0:
    #print(h, w, matrix[h][w])
    if matrix[h][w] == 0:
        end_x = h
        end_y = w
        break
    if matrix[h - 1][w - 1] >= matrix[h - 1][w] - 1 and matrix[h - 1][w - 1] >= matrix[h][w - 1] - 1:
        backTrack.append('\\')
        h -= 1
        w -= 1
    elif matrix[h - 1][w] > matrix[h - 1][w - 1] + 1 and matrix[h - 1][w] >= matrix[h][w - 1]:
        backTrack.append('|')
        h -= 1
    elif matrix[h][w - 1] > matrix[h - 1][w - 1] and matrix[h][w - 1] > matrix[h - 1][w]:
        backTrack.append('-')
        w -= 1
    else:
        print('exception')
        h = 0
        w = 0
#print('end',h,w)
#print(backTrack)
# alignment
seq1 = list(sequence1)
seq2 = list(sequence2)
#print(seq1,seq2)
backTrackRev = backTrack[::-1]
#print(backTrackRev)
for i in range(len(backTrackRev)):
    if backTrackRev[i] == '\\':
        continue
    elif backTrackRev[i] == '|':
        print(seq1)
        seq1.insert(i+h, '-')
        print(i)
    elif backTrackRev[i] == '_':
        seq2.insert(i+w, '-')
#print(seq1)
#print(seq2)
result = []
score = 0
for i in range(h, max_x):
	if seq1[i] == seq2[i]:
		score += 1
		result.append('|')
	elif seq1[i] == '-':
		score -= 1
		result.append(' ')
	else:
		result.append('*')
		score -= 1
score -= h
score -= (len(seq1) - max_x)
print(''.join(seq1[h:max_x]))
print(''.join(result))
print(''.join(seq2[w:max_x]))
print('Alignment score: ', score)
