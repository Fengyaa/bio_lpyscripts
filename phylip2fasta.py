"""
phylip2fasta.py
Usage: python fhylip2fasta.py input_phylip output_fasta
"""

import sys
import textwrap

input_phylip = sys.argv[1]
output_fasta = sys.argv[2]
align = {}


with open(input_phylip, "r") as in_phylip:
    line = [x.strip() for x in in_phylip]
    #basic phylip detect and information collect
    info = line[0].strip().split(" ")
    seq_num = int(info[0])
    seq_length = int(info[1])
    print("{} sequences detected!".format(str(seq_num)))
    print("Length of alignment is {}!".format(str(seq_length)))

    for i in range(1,int(seq_num) + 1):
        j=line[i].strip().split()
        seqname=j[0]
        seq0 = "".join(j[1:])
        seq1 = ""
        for k in range(i,len(line),int(seq_num)):
            if k > i:
                seq1 = seq1 + line[k]
        seq = seq0 + seq1.replace(" ", "")
        align[seqname] = seq


with open(output_fasta, "w") as out_fasta:
    for seqname in align:
        out_fasta.write(">" + seqname + "\n")
        seq = align[seqname]
        seq_lines = textwrap.wrap(seq, width=50)
        for one_line in seq_lines:
            out_fasta.write("{}\n".format(one_line))
        #out_fasta.write(align[seqname] + "\n")
