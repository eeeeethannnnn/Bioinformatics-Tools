#!/usr/bin/env python
# Write your code here.  Print your output to standard out.
import sys
# read argument and file
k = int(sys.argv[1])
with open(sys.argv[2], 'r') as f:
    _fasta = f.read()
#remove first line and '\n'
_fasta = _fasta.split("\n",1)[1]
fasta = _fasta.replace("\n","")
#dict
kmer = {}
seq = ""
for i in range(len(fasta)-k+1):
    seq = fasta[i:i+k]
    if not seq in kmer:
        kmer[seq] = 1
    else:
        kmer[seq] += 1
#sort
output = {}
for key, value in sorted(kmer.items()):
    output[key] = value
    #print("%s\t%s" % (key, value))
    _key = str(key)
    _value = str(value)
    sys.stdout.write(_key+"\t"+_value+"\n")
