#!/usr/bin/env python3
import sys
import argparse

# ./overlapBed.py -i1 <Input file 1> -i2 <Input file 2> -m <INT: minimal overlap> [-j Optional: join the two entries] –o <Outputfile>
# ./overlapBed.py -i1 TE.bed -i2 Intron.bed -m 50 -j -o testOutput
parser = argparse.ArgumentParser()
# input1 should be TE.bed
parser.add_argument('-i1', '--input1', type = str, default = sys.stdin, required = True)
# input2 should be Intron.bed
parser.add_argument('-i2', '--input2', type = str, default = sys.stdin, required = True)
parser.add_argument('-m', '--minimalOverlap', type = str, default = sys.stdin, required = True)
parser.add_argument('-j', '--jointEntries', action='store_true', required = False)
parser.add_argument('-o', '--outputFile', type = str, default = sys.stdin, required = True)
args  = parser.parse_args()
input1 = args.input1
input2 = args.input2
minimal = float(args.minimalOverlap) / 100
joint = False
if args.jointEntries:
    joint = True
output = args.outputFile

te ={}
intron = {}

def storeBED(file, dict):
    for line in file:
        line = line.strip()
        if line.split()[0] not in dict:
            dict[line.split()[0]] = []
        else:
            dict[line.split()[0]].append(line.split())
# read file and store in dictionary
with open(input1, 'r') as file1:
    storeBED(file1, te)
with open(input2, 'r') as file2:
    storeBED(file2, intron)
#print(len(te))
#print(len(intron))
#print('read file complete')
chromosome = []
for i in te:
    chromosome.append(i)
#print(chromosome)
for chr in chromosome:
    #print('chromosome: ', chr)
    overlapStart = 0
    for teIdx in range(len(te[chr])):
        teStart, teStop = int(te[chr][teIdx][1]), int(te[chr][teIdx][2])
        overlap = False
        intronIdx = overlapStart
        while teIdx < len(te[chr]):
            if intronIdx >= len(intron[chr]):
                break
            intronStart, intronStop = int(intron[chr][intronIdx][1]), int(intron[chr][intronIdx][2])
            overlapInt = min(intronStop, teStop) - max(intronStart, teStart)
            if intronStop < teStart and overlap == False:
                intronIdx += 1
                continue
            if overlapInt >= 0: # calculate portion of overlap
                if teStart == teStop:
                    perent = 1
                    overlapInt = 1
                else:
                    percent = overlapInt / (teStop - teStart)
                if overlap == False:
                    overlapStart = intronIdx
                    overlap = True
                if overlap == True and percent < minimal:
                    teIdx += 1
                    continue
                if overlap == True and percent >= minimal:
                    with open(output, 'a+') as aw: # append write
                        if joint == True:
                            aw.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(te[chr][teIdx][0], te[chr][teIdx][1], te[chr][teIdx][2], intron[chr][intronIdx][0], intron[chr][intronIdx][1], intron[chr][intronIdx][2]))
                            print('{}\t{}\t{}\t{}\t{}\t{}'.format(te[chr][teIdx][0], te[chr][teIdx][1], te[chr][teIdx][2], intron[chr][intronIdx][0], intron[chr][intronIdx][1], intron[chr][intronIdx][2]))
                        else:
                            aw.write('t{}\t{}\t{}\n'.format(te[chr][teIdx][0], te[chr][teIdx][1], te[chr][teIdx][2]))
                            print('t{}\t{}\t{}'.format(te[chr][teIdx][0], te[chr][teIdx][1], te[chr][teIdx][2]))
                    intronIdx += 1
                    continue
            if intronStart > teStop and overlap == True:
                break
            else:
                break
