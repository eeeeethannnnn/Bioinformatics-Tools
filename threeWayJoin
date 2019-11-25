#!/usr/bin/env python
# Write your code here.  Print your output to standard out.
import sys
knownGene = str(sys.argv[1]) #col: 1, 2, 4, 5
kgXref = str(sys.argv[2]) #col: 1, 5
infectious = str(sys.argv[3]) #target
#fetch the information in knowGene
known = {}
with open(knownGene, 'r') as file1:
    for line in file1:
        gene = line.split("\t")
        tmp = []
        tmp.extend([gene[1],gene[3],gene[4]]) #chr, start, stop as value
        if gene[0] in known: #use UCSC ID as key
            continue
        else:
            known[gene[0]] = tmp
#fetch the information in kgXref
xRef = {}
with open(kgXref, 'r') as file2:
    for line in file2:
        ref = line.split("\t")
        if not ref[4] in xRef and ref[4] != "": #use gene name as key
            xRef[ref[4]] = ref[0] #UCSC ID as value
        else:
            continue
#search and print
with open(infectious, 'r') as file3:
    #print('{0}\t{1}\t{2}\t{3}'.format('Gene','Chr','Start','Stop'))
    #sys.stdout.write('{0}\t{1}\t{2}\t{3}\n'.format('Gene','Chr','Start','Stop'))
    print("Gene\tChr\tStart\tStop")
    for line in file3:
        tmp = str(line[0:-1])
        if tmp in xRef: # if the target gene in the kgXref
            name = xRef[tmp] #use the UCSC ID from kgXref to fetch detail from knownGene
            #output chr, start of gene and end of gene
            print(tmp,"\t",known[name][0],"\t",known[name][1],"\t",known[name][2],sep="")
            #sys.stdout.write(tmp+"\t"+known[name][0]+"\t"+known[name][1]+"\t"+known[name][2]+"\n")
            #print('{0}\t{1}\t{2}\t{3}'.format(tmp, known[name][0], known[name][1], known[name][2]))
