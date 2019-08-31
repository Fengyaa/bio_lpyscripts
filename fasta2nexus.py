"""
fasta2nexus.py
Usage: python phylip2nexus.py input_nexus output_phylip
"""
import sys
import textwrap

input_fasta = sys.argv[1]
output_nexus = sys.argv[2]
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

with open(output_nexus, "w") as out_nexus:
    out_nexus.write("#NEXUS" + "\n")
    out_nexus.write("BEGIN DATA;" + "\n")
    out_nexus.write(" DIMENSIONS NTAX=" + str(seq_num) + " NCHAR=" + str(seq_length) + ";\n")
#     DNA_CHARS = ["A", "G", "T", "C", "-", "?", "N", "a", "g", "t", "c", "n", " "]
#     if seq in DNA_CHARS: ##need revision
#         out_nexus.write("FORMAT DATATYPE=DNA INTERLEAVE=yes GAP=-;" + "\n")
#     else:
#         out_nexus.write("FORMAT DATATYPE=PROTEIN INTERLEAVE=yes GAP=-;" + "\n")
    out_nexus.write("FORMAT DATATYPE=DNA INTERLEAVE=yes GAP=-;" + "\n")
    for seqname in align:
        seq = align[seqname]
        seq_lines = textwrap.wrap(seq, width=50)
        while len(seqname) <= 9:
                seqname = seqname + " "
        out_nexus.write("[Name: " + seqname + "Len: " + str(seq_length) + "]\n")
    
    out_nexus.write("\nMATRIX\n")
   
    for i in range(0, len(seq_lines)):
        for seqname in align:
            seq = align[seqname]
            seq_lines = textwrap.wrap(seq, width=50)
            while len(seqname) <= 10:
                seqname = seqname + " "
            out_nexus.write(seqname + " ".join(textwrap.wrap(seq_lines[i], width = 10)) + "\n")
        out_nexus.write("\n")
    out_nexus.write(";\nEND;\n")


