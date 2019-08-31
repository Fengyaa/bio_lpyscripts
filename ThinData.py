#!/usr/bin/env python3
"""
    Created on 2019-6-20
    Usage:
    python ThinData.py input.fasta output.fasta
"""
import sys
import time

input_fasta = sys.argv[1]
output_fasta = sys.argv[2]
step = 10 #this means take one base every ten nucleotides

input_alignment = open(input_fasta,"r")
output_fasta = open(output_fasta,"w")
time_start = time.time()

for line in input_alignment:
    if line.startswith(">"):
        output_fasta.write(line.strip()+"\n")
    else:
        seq = line.strip()
        lenth = len(seq)
        counts = range(1,lenth,step)
        for y in counts:
            output_fasta.write(seq[y])
        output_fasta.write("\n")

input_alignment.close()
output_fasta.close()

time_end = time.time()
print("Completed after {}s!".format(str(time_end - time_start)))
