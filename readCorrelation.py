# read matrix
with open('correlation_20191121.txt', 'r') as readDB:
    read = readDB.read()
contentDB = read.split('\n')
matrixLen = len(contentDB)
matrixDB = []
for line in contentDB:
    col = line.split('\t')
    matrixDB.append(col)

# read target
with open('targetGene.txt', 'r') as readTarget:
    read = readTarget.read()
contentTarget = read.split('\n')
#print(contentTarget)
#print(len(contentTarget))

#for i in range(1, len(matrixDB)):
#    if matrixDB[i][0] in contentTarget:
#        for j in range(len(matrixDB[i])):
#            print(matrixDB[i][j])

with open('ppi6.txt', 'w+') as ppiWrite:
    for i in range(1, len(matrixDB)):
        if matrixDB[i][0] in contentTarget:
            for j in range(1, len(matrixDB[i])):
                if matrixDB[0][j] in contentTarget:
                    if matrixDB[i][j] != '1':
                        print('%s\t%s\t%s' %(matrixDB[i][0], matrixDB[0][j], matrixDB[i][j]))
                        ppiWrite.write('%s\t%s\t%s\n' %(matrixDB[i][0], matrixDB[0][j], matrixDB[i][j]))
                    else:
                        continue
