import re
import numpy as np

Chain1 = "E"
# chainOne 
Chain2 = "I"
# chainTwo
dist_threshold = 10
inputfile = "1atp.pdb"

# read file
with open(inputfile,'r') as f:
    file = f.read()

## data filtering

# chain determination 
content = file.split('\n')
chainOne = []
chainTwo = []
for line in range(len(content)):
    if content[line].startswith('ATOM'):
        tmp = content[line].split()
        if tmp[2] == 'CA' and tmp[4] == Chain1:
            chainOne.append(tmp)
        elif tmp[2] == 'CA' and tmp[4] == Chain2:
            chainTwo.append(tmp)

#distance calculation
_interface = []

for i in range(len(chainOne)):
    for j in range(len(chainTwo)):
        distance = ((abs(float(chainOne[i][6]) - float(chainTwo[j][6]))) ** 2 + (abs(float(chainOne[i][7]) - float(chainTwo[j][7]))) ** 2 + (abs(float(chainOne[i][8]) - float(chainTwo[j][8]))) ** 2) ** (1/2)
        if distance < dist_threshold:
            print(chainOne[i][4], ':', chainOne[i][3], '(', chainOne[i][5],')', ' interacts with ', chainTwo[j][4], ':', chainTwo[j][3], '(', chainTwo[j][5],')', sep='')
            # new list for interface residue
            if chainOne[i] not in _interface:
                _interface.append(chainOne[i])
            if chainTwo[j] not in _interface:
                _interface.append(chainTwo[j])
                
#codes here
# secondary structures determination
interface = sorted(_interface, key=lambda x:x[4])
second = []

for line in range(len(content)):
    if content[line].startswith('HELIX') or content[line].startswith('SHEET'):
        tmp = content[line].split()
        second.append(tmp)

chain_one_helix = 0
chain_one_sheet = 0
chain_two_helix = 0
chain_two_sheet = 0

for i in range(len(interface)):
    for j in range(len(second)):
        if second[j][4] == interface [i][4] == Chain1 and second[j][0] == 'HELIX':
            if int(interface[i][5]) <= int(second[j][8]) and int(interface[i][5]) >= int(second[j][5]):
                chain_one_helix += 1
        elif second[j][4] == interface [i][4] == Chain1 and second[j][0] == 'SHEET':
            if int(interface[i][5]) <= int(second[j][8]) and int(interface[i][5]) >= int(second[j][5]):
                chain_one_sheet += 1
        elif second[j][4] == interface [i][4] == Chain2 and second[j][0] == 'HELIX':
            if int(interface[i][5]) <= int(second[j][8]) and int(interface[i][5]) >= int(second[j][5]):
                chain_two_helix += 1
        elif second[j][4] == interface [i][4] == Chain2 and second[j][0] == 'SHEET':
            if int(interface[i][5]) <= int(second[j][8]) and int(interface[i][5]) >= int(second[j][5]):
                chain_two_helix += 1
print('chain:', Chain1)
print(chain_one_helix, '/', len(interface), ' of the interface amino acids lying on alpha helices.',sep='')
print(chain_one_sheet, '/', len(interface), ' of the interface amino acids lying on beta sheets.',sep='')
print('chain:', Chain2)
print(chain_two_helix, '/', len(interface), ' of the interface amino acids lying on alpha helices.',sep='')
print(chain_two_sheet, '/', len(interface), ' of the interface amino acids lying on beta sheets.',sep='')

# determine the closest interface atom of the same chain to the right
chainFirst = []
chainSecond = []
for i in range(len(interface)):
    if interface[i][4] == Chain1:
        chainFirst.append(interface[i])
    elif interface[i][4] == Chain2:
        chainSecond.append(interface[i])
        
for i in range(len(chainFirst) - 1):
    closestDistance = int(chainFirst[i+1][5]) - int(chainFirst[i][5])
    print(chainFirst[i][3], ': closest', chainFirst[i + 1][3], 'at distance', closestDistance, sep=' ')
chainSecond.sort()
for i in range(len(chainSecond) - 1):
    closestDistance = int(chainSecond[i+1][5]) - int(chainSecond[i][5])
    print(chainSecond[i][3], ': closest', chainSecond[i + 1][3], 'at distance', closestDistance, sep=' ')
