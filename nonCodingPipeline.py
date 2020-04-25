import argparse
import sys
import os

def gff2fasta(file_1, file_2, out_file):
	if os.path.exists(file_2):
		fasta_files = os.listdir(file_2)
	if os.path.exists(file_1):
		gff_files = os.listdir(file_1)

	for gff_file in gff_files:
		#print(gff_file)
		fasta_con = open(os.path.join(file_2, gff_file.split('.')[0] + '.fasta'), 'r')
		fasta = fasta_con.readlines()[1:]
		out_fasta = open(os.path.join(out_file, gff_file.split('.')[0] + '.fasta'), 'w+')
		#print(fasta)
		node_list = []
		seq = ''
		for line in fasta:
			line = line.strip()
			if line.startswith('>'):
				node_list.append(seq)
				seq = ''
				continue
			seq+=line;
		node_list.append(seq)
		print('node_list length',len(node_list))
		fasta_con.close()
		#print(node_list)
		gff_f = open(os.path.join(file_1, gff_file), 'r')
		gff = gff_f.readlines()
		#print(gff)
		for line in gff:
			line = line.strip().split('\t')
			node_name = line[0]
			node = int(node_name.split('_')[1]) - 1
			print(str(node))
			rna = line[2]
			star = int(line[3])
			end = int(line[4])
			print(len(node_list))
			print(len(node_list[node]))
			my_seq = node_list[node][star - 1 : end - 1]
			print(my_seq)

			out_fasta.write('>Node:' + node_name + '\tRNA_type:' + rna + '\tStart:' + str(star) + '\tEnd:' + str(end) + '\n')
			out_fasta.write(my_seq + '\n')
		gff_f.close()

parser=argparse.ArgumentParser()
parser.add_argument("-i", "--Input_dir", help = 'input gff3', required = True)
parser.add_argument("-o", "--Output_dir", help = 'output file', required = True)

args = parser.parse_args()
input_dir = args.Input_dir
out_dir = args.Output_dir # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding
gff_dir = out_dir + "/gff" # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff
if os.path.exists(gff_dir):
	print("gff folder exists")
else:
    print('=====nonCoding Start From Here=====')
	print("create gff folder")
	os.system('mkdir ' + gff_dir)

infernal_dir = gff_dir + '/infernal' # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff/infernal

infernal_raw_dir = infernal_dir + "/raw" # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff/infernal/raw
infernal_gff_dir = infernal_dir + "/gff" # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff/inferal/gff
fasta_dir = out_dir + '/fasta' # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/fasta
if os.path.exists(infernal_dir):
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/infernal/Rfam/runinfernal.sh -f '+ input_dir + ' -o ' + infernal_raw_dir)
else:
    os.system('mkdir ' + infernal_dir)
    os.system('mkdir ' + infernal_raw_dir)
    os.system('mkdir ' + infernal_gff_dir)
    os.system('mkdir ' + fasta_dir)
    os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/infernal/Rfam/runinfernal.sh -f '+ input_dir + ' -o ' + infernal_raw_dir)
    os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/infernal/rungff.sh -f ' + infernal_raw_dir + ' -o ' + infernal_gff_dir)

gff2fasta(infernal_gff_dir, input_dir, fasta_dir)


rnammer_dir = gff_dir + '/rnammer' # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff/rnammer/
if os.path.exists(rnammer_dir):
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/RNAmmer/runrnammer.sh -f '+ input_dir + ' -o ' + rnammer_dir)
else:
	os.system('mkdir ' + rnammer_dir)
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/RNAmmer/runrnammer.sh -f '+ input_dir + ' -o ' + rnammer_dir)

aragorn_dir = gff_dir + '/aragorn' # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff/aragorn
if os.path.exists(aragorn_dir):
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/runaragorn.sh -f '+ input_dir + ' -o ' + aragorn_dir)
else:
	os.system('mkdir ' + aragorn_dir)
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/runaragorn.sh -f '+ input_dir + ' -o ' + aragorn_dir)

barnap_dir = gff_dir + '/barnap' # /home/projects/group-c/Team3-GenePrediction/forGit/adding_non-coding/ToolOutputs/nonCoding/gff/barrnap
if os.path.exists(barnap_dir):
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/runbarnap.sh  -f '+ input_dir + ' -o ' + barnap_dir)
else:
	os.system('mkdir ' + barnap_dir)
	os.system('/home/projects/group-c/Team3-GenePrediction/Python_Scripts/ToolOutputs/runbarnap.sh -f '+ input_dir + ' -o ' + barnap_dir)
