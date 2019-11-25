#!/usr/bin/env python
# Shebang line here
import sys
import argparse
import re
#from string import digits
# Your code here

# command line input argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--input1', type = int, default = 70, required = False) #without -f from command fold = 70
parser.add_argument('-i', '--input2', type = str, default = sys.stdin, required = True)
args  = parser.parse_args()
fold = args.input1
fileName = args.input2

# initialize a class to define input file
class DefineFile:
    #attributes of object
    content = []
    output = []

    # read file and store in an object
    def readFile(self, fileName):
        #print('read file called', fileName)
        with open(fileName, 'r') as r:
            readFile = r.read()
            #readFile = str(_readFile, encoding = "utf-8")
            line = readFile.split('\n')
            for i in range(len(line)):
                if line[i] == '':
                    continue
                else:
                    self.content.append(line[i])
                    #print(line[i])
        return self.content

    # define file type by some key text in content
    def checkType(self):
        #print('check type called')
        if re.search('@', self.content[0]):
            #print('fileType: fastq')
            self.fastq()
        elif re.search('#MEGA', self.content[0]):
            #print('fileType: mega')
            self.mega()
        elif re.search('ID', self.content[0]):
            #print('fileType: embl')
            self.embl()
        elif re.search('LOCUS', self.content[0]):
            #print('fileType: gb')
            self.gb()

    # fastq handling save gene name & gene sequence then discard other information
    def fastq(self):
        #print('fastq called')
        count = 1
        newSequence = False
        for i in range(len(self.content)):
            if count % 4 == 1:
                self.content[i] = self.content[i].strip('@')
                if self.content[i] not in self.output:
                    self.output.append(self.content[i])
                    newSequence = True
            if count % 4 == 2 and newSequence :
                self.output.append(''.join(self.content[i]))
            count += 1

    # mega handling save gene name & gene sequence then discard other information
    def mega(self):
        #print('mega called')
        flag = 0
        for i in range(2, len(self.content)):
            if self.content[i].startswith('#'):
                self.output.append(self.content[i])
                self.output.append(' ')
                flag = len(self.output)
                tmp = ''
            else:
                tmp += self.content[i].strip('\n')
                self.output[flag-1] = tmp

    # embl handling save gene name & gene sequence then discard other information
    def embl(self):
        seqStart = False
        sequence = ''
        #print('embl called')
        for i in range(len(self.content)):
            if re.search('AC', self.content[i]):
                tmp = self.content[i].split()
                self.output.append(tmp[1].strip(';'))
            if seqStart:
                if re.search('//', self.content[i]):
                    continue
                else:
                    sequence += self.content[i].replace(' ', '')
            if re.search('SQ', self.content[i]):
                seqStart = True
        # sequence = sequence.translate(None, digits) ###need to import digits from string (but much faster)
        sequence = ''.join(i for i in sequence if not i.isdigit())
        self.output.append(sequence.upper())

    # gb handling save gene name & gene sequence then discard other information
    def gb(self):
        seqStart = False
        sequence = ''
        #print('embl called')
        for i in range(len(self.content)):
            if re.search('LOCUS', self.content[i]):
                tmp = self.content[i].split()
                self.output.append(tmp[1])
            if seqStart:
                if re.search('//', self.content[i]):
                    continue
                else:
                    sequence += self.content[i].replace(' ', '')
            if re.search('ORIGIN', self.content[i]):
                seqStart = True
        # sequence = sequence.translate(None, digits) ###need to import digits from string (but much faster)
        sequence = ''.join(i for i in sequence if not i.isdigit())
        self.output.append(sequence.upper())

    def printSelf(self):
        print('FOLD:', fold)
        print('FileName: ', fileName)
        for i in range(len(self.output)):
            if i % 2 == 0:
                print('\n', '>', end = '')
                print(self.output[i])
            else:
                seqList = list(self.output[i])
                for j in range(len(seqList)):
                    if j > 0 and j % fold == 0:
                        print('\n', end = '')
                    if j % 10 == 0:
                        print('|', end = '')
                    print(seqList[j], end = '')
        print('\n')
        #for i in range(len(self.content)):
        #    print(self.content[i])

    #examine sequence is nucleotide acids sequence or amino acids sequence and write into file
    def writeFile(self, fileName):
        isNucleotide = True
        if re.search('[^ATCGNatcgn]', self.output[1]):
            isNucleotide = False
        if 'fastq' in fileName:
            if isNucleotide:
                newFileName = fileName.replace('fastq', 'fna')
            else:
                newFileName = fileName.replace('fastq', 'faa')
        else:
            if isNucleotide:
                newFileName = fileName + '.fna'
            else:
                newFileName = fileName + '.faa'

        with open(newFileName, 'w') as w:
            for i in range(len(self.output)):
                if i % 2 == 0:
                    w.write('>')
                    w.write(self.output[i] + '\n')
                else:
                    seqList = list(self.output[i])
                    for j in range(len(seqList)):
                        if j > 0 and j % fold == 0:
                            w.write('\n')
                        #if j % 10 == 0:
                        #    w.write('|')
                        w.write(seqList[j])
                    w.write('\n')

#main()
DefineFile().readFile(fileName)
DefineFile().checkType()
#DefineFile().printSelf()
DefineFile().writeFile(fileName)
