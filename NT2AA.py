from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

inputfile ="test.fasta"
f = open(inputfile, "r")
seq = f.readlines()

end = True
aminoAcidSeq = {}
header = ""
i = 0
tmp = ""
while i < len(seq):
    if i == 0 and seq[i].startswith('>'):
        header = seq[i]
        tmp = ""
    elif seq[i].startswith('>'):
        translate = Seq(tmp)
        aminoAcidSeq[header] = str(translate.translate().strip('*'))
        header = seq[i]
        tmp = ""
    else:
        tmp += seq[i].strip('\n')
    i += 1

translate = Seq(tmp)
aminoAcidSeq[header] = str(translate.translate().strip('*'))
f = open("testOutput.fasta", "w")
for key, value in aminoAcidSeq.items():
    f.write(key)
    f.write(value)
    f.write('\n')
f.close()
"""

for key, value in aminoAcidSeq.items():
    print(key, value)
"""
