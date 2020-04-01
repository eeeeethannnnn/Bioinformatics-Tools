inputfile =".fasta"
f = open(inputfile, "r")
seq = f.readlines()
#for i in range(len(seq)):
#    print(seq[i].strip("\n"))
header = []
i = 0
sequence = []
headerCount = 0
tmp = ""
while i < len(seq):
    #print(seq[i])
    if i == 0 and seq[i].startswith('>'):
        header.append(seq[i].strip('\n'))
        headerCount += 1
    elif seq[i].startswith('>'):
        sequence.append(tmp)
        tmp = ""
        header.append(seq[i].strip('\n'))
        headerCount += 1
    else:
        tmp += seq[i].strip('\n')
    i += 1
sequence.append(tmp)




newFile = "split"
m = 0
n = 1172 #how many sequence per file
plus = 1172 #how many sequence per file
for i in range(1, 11):
    new = newFile + str(i) + ".fasta"
    f = open(new, "w")
    print(new)
    for j in range(m, n):
        f.write(header[j])
        f.write('\n')
        f.write(sequence[j])
        f.write('\n')
    f.close()
    m = n
    n += plus
