infile = open("data (1).csv","r")
#your code here
table = infile.read()
table = table.split()
matrix = []
total = 0
for i in range(1, len(table)):
    tmp = table[i].split(',')
    matrix.append(tmp)
for i in range(len(matrix)):
    for j in range(1, len(matrix[i])):
        decimal = float(matrix[i][j])
        total += decimal
    matrix[i].append(total/4)
    total = 0

print('Part (A)(1)')
for i in range(len(matrix)):
    print(matrix[i][0],matrix[i][5],sep='\t')
distance = [[]]
sort = sorted(matrix,key=lambda index:index[5], reverse=True)
print('\nPart (A)(2)')
for i in range(len(sort)):
    print(sort[i][0])
    distance[0].append(sort[i][0])
#print(distance)
infile = open("data (1).csv","r")
#your code here
table = infile.read()
table = table.split()
matrix = []
total = 0
for i in range(1, len(table)):
    tmp = table[i].split(',')
    matrix.append(tmp)

for i in range(len(matrix)):
    matrix[i].append(total)

print('Part (B)(1)')

print('Ranking by column2: Molecular_Function')    
sort = sorted(matrix,key=lambda index:index[1], reverse=True)
for i in range(len(sort)):
    sort[i][5] += len(sort) - i
for i in range(len(sort)-1):
    start = i
    count = 1
    avg = 0
    total = len(sort) - i
    if i+1 < 13 and sort[i][1] != sort[i+1][1]:
        continue
    else:
        while i != 12 and sort[i][1] == sort[i+1][1]:
            count += 1
            total += len(sort) - (i + 1)
            avg = total / count
            i += 1
        while count != 0:
            sort[start][5] = avg
            count -= 1
            start += 1       
    if i >= len(sort)-1:
        break
for i in range(len(sort)):
    print(sort[i][0], sort[i][1], sort[i][5], sep='\t')

print('\nRanking by column3: Biological Process')    
sort = sorted(matrix,key=lambda index:index[2], reverse=True)
for i in range(len(sort)):
    sort[i].append(len(sort)-i)
for i in range(len(sort)-1):
    start = i
    count = 1
    avg = 0
    total = len(sort) - i
    if i+1 < 13 and sort[i][2] != sort[i+1][2]:
        continue
    else:
        while i != 12 and sort[i][2] == sort[i+1][2]:
            count += 1
            total += len(sort) - (i + 1)
            avg = total / count
            i += 1
        while count != 0:
            sort[start][6] = avg
            count -= 1
            start += 1       
    if i >= len(sort)-1:
        break
for i in range(len(sort)):
    print(sort[i][0], sort[i][2], sort[i][6], sep='\t')

print('\nRanking by column4: Cellular Component')    
sort = sorted(matrix,key=lambda index:index[3], reverse=True)
for i in range(len(sort)):
    sort[i].append(len(sort)-i)
for i in range(len(sort)-1):
    start = i
    count = 1
    avg = 0
    total = len(sort) - i
    if i+1 < 13 and sort[i][3] != sort[i+1][3]:
        continue
    else:
        while i != 12 and sort[i][3] == sort[i+1][3]:
            count += 1
            total += len(sort) - (i + 1)
            avg = total / count
            i += 1
        while count != 0:
            sort[start][7] = avg
            count -= 1
            start += 1       
    if i >= len(sort)-1:
        break
for i in range(len(sort)):
    print(sort[i][0], sort[i][3], sort[i][7], sep='\t')

print('\nRanking by column5: Domain')    
sort = sorted(matrix,key=lambda index:index[4], reverse=True)
for i in range(len(sort)):
    sort[i].append(len(sort)-i)
    #print(sort[i][0], sort[i][4], sort[i][8], sep='\t')
i = 0
#for i in range(len(sort)-1):
while i < len(sort)-1:
    #print('==new for loop===, i:',i)
    start = i
    count = 1
    avg = 0
    total = len(sort) - i
    if i+1 < 13 and sort[i][4] != sort[i+1][4]:
        i += 1
        continue
    else:
        while i != 12 and sort[i][4] == sort[i+1][4]:
            count += 1
            total += len(sort) - (i + 1)
            avg = total / count
            #print('first while total:', total, 'count', count)
            i += 1
        while count != 0:
            sort[start][8] = avg
            #print(sort[start][0],sort[start][4],sort[start][8],sep='\t')
            count -= 1
            start += 1
    #print('for loop end i:', i)
    if i >= len(sort)-1:
        break
for i in range(len(sort)):
    print(sort[i][0], sort[i][4], sort[i][8], sep='\t')
print('\nPart (B)(2)')
print('Ranking by aggregate ranking')
sum = 0
for i in range(len(sort)):
    sort[i].append(sort[i][5]+sort[i][6]+sort[i][7]+sort[i][8])

sort = sorted(matrix,key=lambda index:index[9], reverse=True)
tmp = []
for i in range(len(sort)):
    print(sort[i][0])
    tmp.append(sort[i][0])
distance.append(tmp)
#print(distance)

#Part C Kendall’s and Spearman distances
print('Part (C) Kendall’s and Spearman distances')
def Kendalls(string1, string2) :
    str1 = list(string1)
    str2 = list(string2)
    c = 0
    for i in range(len(str2)-1):
        for j in range(len(str2)-i):
            if str1[j] != str2[j]:
                str2[j], str2[j+1] = str2[j+1], str2[j]
                #print(str2)
                c += 1
            else :
                continue
    return c
print('Kendalls distance is:',Kendalls(distance[0],distance[1]))

def Spearman(string1,string2):
    str1 = list(string1)
    str2 = list(string2)
    c = 0
    for i in range(len(str2)):
        if str1[i] != str2[i]:
            idx = str1.index(str2[i])
            c += abs(idx - i)
        else :
             continue
    return c
print('Spearman distance is:',Spearman(distance[0],distance[1]))
