#!/bin/bash
# Place your gatech userame in the below export
export NAME="scheng98"

get_input () {
	#local_path=$(dirname "$0")
	echo "Get input"
	echo "^^^^^^^^^"
	while getopts "a:b:r:eo:zvif:h" opt; do

		case "$opt" in
			a)
				reads1=$OPTARG
				;;
			b)
				reads2=$OPTARG
				;;
			r)
				ref=$OPTARG
				;;
			e)
				realign=1
				;;
			o)
				output=$OPTARG
				;;
			z)
				gunzip=1
				;;
			v)
				v=1
				;;
			i)
				index=1
				;;
			f)
				millsFile=$OPTARG
				;;
			\?) 
				echo "Please use flags:[-a], [-b], [-r], [-e], [-o], [-f], [-z], [-v], [-i], [-h]"
      				;;
			:)
      				echo "Invalid option: $OPTARG requires an argument"
      				;;
			h)
				echo "bash <bashfile.bash> -a reads1 -b reads2 -r reference -e -o <outputName> -zvi -f millsFile"
#bash snp_pipeline.bash -a D2-DS3_paired1.fq -b D2-DS3_paired2.fq -r chr17.fa -e -o scheng98 -zvi -f Mills_and_1000G_gold_standard.indels.hg38.vcf				
				exit 0
		esac
	done
	echo "realign: $realign"
	echo "v: $v"
	echo "index: $index"
	echo "gunzip: $gunzip"
	echo "===================================="
	echo ""
}
    

check_files () {
	echo "Check Files"	
	echo "^^^^^^^^^^^"
	if  [ -f "$reads1" ]; then
		echo "reads1: $reads1"
	else
		echo "reads1 is invalid or missing"
		exit 1
	fi

	if  [ -f "$reads2" ]; then 
		echo "reads2: $reads2"
	else
		echo "reads2 is invalid or missing"
		exit 1
	fi

	if  [ -f "$ref" ]; then
		echo "reference: $ref"
	else
		echo "reference is invalid or missing"
		exit 1
	fi

	if  [ -f "$millsFile" ]; then 
		echo "millsFile: $millsFile"
	else
		echo "millsFile is invalid or missing"
		exit 1
	fi

	if [  -f  "$output" ]; then
		echo "Output file exists. Do you want to overwrite? [Y/N]"
		read -n 1 out_opt
		if [ "$out_opt" == "Y" ];then
			echo ''
			echo "Overwrite the output"
		else
			echo '' 
			echo "Try another output name."
			exit 1;
		fi
	else		
		echo "outputName: $output"
	fi
	echo "===================================="
	echo ""
}

prepare_temp () {
	echo "Prepare temp directory"
	echo "^^^^^^^^^^^^^^^^^^^^^^"
	mkdir -p ./tmp
	
	if [ ! -z "$v" ];then		
		echo "Now create the temporary directory!"
	fi
	echo "==================================="
	echo ""
}


mapping () {
	if [ ! -z "$v" ];then
		echo "Mapping"
		echo "^^^^^^^"
	fi
	#use bwa as reference
	bwa index $ref
	if [ ! -z "$v" ];then
		echo "Index reference finish"
		echo "----------------------"
	fi

	#bwa mem ref.fa reads.fq > aln-se.sam
#-R STR	Complete read group header line. ’\t’ can be used in STR and will be converted to a TAB in the output SAM. The read group ID will be attached to every read in the output. An example is ’@RG\tID:foo\tSM:bar’. [null]
	echo "bwa mem -R"
	echo "----------"	
	bwa mem -R '@RG\tID:foo\tSM:bar\tLB:library1' $ref $reads1 $reads2 > ./tmp/bwa_mem.sam
	if [ ! -z "$v" ];then
		echo "bwa mem finish"
		echo "--------------"
	fi
	#samtools fixmate [-rpcm] [-O format] in.nameSrt.bam out.bam
	#-O FORMAT Write the final output as sam, bam, or cram.
	echo "samtools fixmate -O"
	echo "-------------------"
	samtools fixmate -O bam ./tmp/bwa_mem.sam ./tmp/samtools_fixmate.bam
	if [ ! -z "$v"  ];then
		echo "fixmate finish"
		echo "--------------"
	fi

	#samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format] [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
	echo "samtools sort -O -o -T"
	echo "----------------------"	
	samtools sort -O bam -o ./tmp/samtools_sorted.bam -T tmp ./tmp/samtools_fixmate.bam
	samtools index ./tmp/samtools_sorted.bam

	if [ ! -z "$v" ];then
		echo "Sort finish"
	fi
	echo "==================================="
	echo ""
}

improvement () {
	if [ ! -z "$v" ];then
		echo "Improvement"
		echo "^^^^^^^^^^^"
	fi

	if [ ! -z "$realign" ] ;then
		
		if [ ! -z "$v" ];then
			echo "Now in realignment"
			echo "------------------"
		fi


		#samtools faidx <ref.fasta> [region1 [...]]
		samtools faidx $ref

		#https://broadinstitute.github.io/picard/command-line-overview.html
		#java -jar picard.jar CreateSequenceDictionary -R reference.fasta -O reference.dict ###new syntax###
		java -jar ./lib/picard.jar CreateSequenceDictionary R=$ref O=chr17.dict

		#Function for improving the number of miscalls


		#https://software.broadinstitute.org/gatk/documentation/article?id=7156
		echo "java calls GATK realigner target creator"
		echo "----------------------------------------"
		java -Xmx2g \
			-jar ./lib/GenomeAnalysisTK.jar \
			-T RealignerTargetCreator \
			-R $ref \
			-I ./tmp/samtools_sorted.bam \
			-o ./tmp/realignertargetcreator.bam \
			-known $millsFile  2>> ./output/scheng98.log #error to log
		#https://software.broadinstitute.org/gatk/documentation/tooldocs/3.8-0/org_broadinstitute_gatk_tools_walkers_indels_IndelRealigner.php
		echo "java calls GATK indel realigner"	
		echo "-------------------------------"
		java -jar ./lib/GenomeAnalysisTK.jar \
			-T IndelRealigner \
			-R $ref \
			-I ./tmp/samtools_sorted.bam \
			-o ./tmp/gatk_realigned.bam \
			-targetIntervals ./tmp/IndelRealigner.intervals \
			-known $millsFile 2>> ./output/scheng98.log #error to log
	fi

	if [ ! -z "$index"  ] ;then
		if [ ! -z "$realign" ];then
			samtools index ./tmp/gatk_realigned.bam
		fi
	fi
	echo "==================================="
	echo ""
}

call_variants () {	
	if [ ! -z "$v"  ];then
		echo "Call Variants"
		echo "^^^^^^^^^^^^^"
	fi

	output_temp=scheng98.vcf.gz
	#https://samtools.github.io/bcftools/bcftools.html#mpileup
	if [ -f ./tmp/gatk_realigned.bam ]; then
		echo "bcftools output uncompressed BCF referenced by gatk_realigned.bam"
		echo "-----------------------------------------------------------------"
		bcftools mpileup -Ou -f $ref ./tmp/gatk_realigned.bam | bcftools call -vmO z -o $output_temp || exit 1
	else
		echo "bcftools output uncompressed BCF referenced by samtools_sorted.bam"
		echo "------------------------------------------------------------------"
		bcftools mpileup -Ou -f $ref ./tmp/samtools_sorted.bam | bcftools call -vmO z -o $output_temp || exit 1
	fi

	ls -alh ./output


	if [ ! -z "$gunzip" ];then 
		cp $output_temp ./output/"$output".vcf.gz
		
	else 
		gunzip -c $output_temp > ./output/"$output".vcf
	fi

}

main() {
	# Function that defines the order in which functions will be called
	# You will see this construct and convention in a lot of structured code.
	
	# Add flow control as you see appropriate
	get_input "$@"
	check_files # Add arguments here
	prepare_temp
	#mapping # Add arguments here
	improvement # Add arguments here
	call_variants # Add arguments here
}

# Calling the main function
main "$@"
zcat scheng98.vcf.gz | awk '! /\#/' |awk '{gsub(/^chr/,""); print}'| awk '{ print $1"\t"$2"\t"$2+length($5)-length($4)"\t"length($5)-length($4);}'| awk '{if ($4 != 0) print >"indels.txt"; else print >"snps.txt"}'

# DO NOT EDIT THE BELOW FUNCTION
bats_test (){
    command -v bats
}
# DO NOT EDIT THE ABOVE FUNCTION
