
"""
fasta to phylip
Usage: python fasta2phylip.py input_fasta output_phylip
"""

import sys
import textwrap

input_fasta = sys.argv[1]
output_phylip = sys.argv[2]
align = {}

with open(input_fasta, "r") as in_fasta:
    seq = ""
    seqname = ""
    seq_num = 0
    #for line in input:
    for line in in_fasta:
        if line[0] == ">":
            seqname = line.strip(">").strip()
            seq_num = seq_num + 1
            seq = ""
        else:
            seq = seq + line.strip()
        seq_length = len(seq)
        align[seqname] = seq
    print("{} sequences detected!".format(str(seq_num)))
    print("Length of alignment is {}!".format(str(seq_length)))


with open(output_phylip, "w") as out_phylip:
    out_phylip.write(" " + str(seq_num) + " " + str(seq_length) + "\n")
    for seqname in align:
        seq = align[seqname]
        seq_lines = textwrap.wrap(seq, width=50)
        while len(seqname) <= 11:
            seqname = seqname + " "
        #line_one =textwrap.wrap(seq_lines[0], width = 10)
        #out_phylip.write(seqname + " ".join(textwrap.wrap(seq_lines[0], width = 10)) + "\n")
        out_phylip.write(seqname + seq_lines[0] + "\n") 
        
    for i in range(1, len(seq_lines)):
        for seqname in align:
            seq = align[seqname]
            seq_lines = textwrap.wrap(seq, width=50)
            #out_phylip.write(" ".join(textwrap.wrap(seq_lines[i], width = 10)) + "\n")
            out_phylip.write(seq_lines[i] + "\n")
