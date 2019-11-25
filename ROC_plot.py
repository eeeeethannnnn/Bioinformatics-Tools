import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

dadaResult = []
with open('candidatesGene.txt', 'r') as readCan:
    content = readCan.read()
candidate = content.split('\n')
candidateLen = len(candidate)
#for i in range(len(candidate)):
#    print(candidate[i])
#print(candidateLen)

#DADA alignment result
with open('dadaRankingResult.txt', 'r') as dada:
    read = dada.read()
dadaResult = read.split('\n')
for i in range(len(dadaResult)):
    dadaResult[i] = dadaResult[i].replace(' ', '')
    dadaResult[i] = dadaResult[i].replace('\'', '')
    dadaResult[i] = dadaResult[i].strip('{')
    dadaResult[i] = dadaResult[i].strip('}')
    #print(dadaResult[i])
dadaLen = len(dadaResult)
#print(dadaLen)

ranking = []
for i in range(dadaLen):
    tmp = []
    tmp.append(dadaResult[i])
    if i < dadaLen:
        tmp.append(1)
    else:
        tmp.append(0)
    if dadaResult[i] in candidate:
        tmp.append(1)
    else:
        tmp.append(0)
    ranking.append(tmp)


#for i in range(len(ranking)):
#    print(ranking[i])
rankingLen = len(ranking)
print(rankingLen)
for i in range(rankingLen):
    print(ranking[i][0], ranking[i][1], ranking[i][2], sep = '\t')
    
ideal = np.array([0] * rankingLen)
actual = np.array([0] * rankingLen)
for i in range(rankingLen):
    ideal[i] = int(ranking[i][1])
    actual[i] = int(ranking[i][2])

for i in range(rankingLen):
    print(ideal)
    print(actual)

fpr, tpr, thresholds = metrics.roc_curve(ideal, actual, pos_label = 1)
auc = metrics.auc(fpr, tpr)
print('True Positive Rate: ', tpr)
print(type(tpr))
print('False Positive Rate: ',fpr)
print('Area Under Curve = %0.2f' % auc)

plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
