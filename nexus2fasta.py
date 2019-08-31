"""
nexus2fasta.py
Usage: python nexus2fasta.py input_nexus output_fasta

"""

import sys
import textwrap

input_nexus = sys.argv[1]
output_fasta = sys.argv[2]
align = {}


with open(input_nexus, "r") as in_nexus:
    line = [x.strip() for x in in_nexus]
    dimensions = line[2].strip(";").split()
    seq_num_p = dimensions[1].split("=")
    seq_num = int(seq_num_p[1])
    seq_length_p = dimensions[2].split("=")
    seq_length = int(seq_length_p[1])
    format = line[3].strip().strip(";").split()
    datatype_p = format[1]
    datatype = datatype_p[1]
    print("{} sequences detected!".format(str(seq_num)))
    print("Length of alignment is {}!".format(str(seq_length)))

    p = line.index("MATRIX")
    for i in range(1, seq_num + 1):
        a = line[p + i].split()
        seqname = a[0]
        seq = ""
        for j in range(p + i, len(line) - 2, seq_num + 1):
            b = line[j].split()
            seq = seq + "".join(b[1:])
        align[seqname] = seq


with open(output_fasta, "w") as out_fasta:
    for seqname in align:
        out_fasta.write(">" + seqname + "\n")
        seq = align[seqname]
        seq_lines = textwrap.wrap(seq, width=50)
        for one_line in seq_lines:
            out_fasta.write("{}\n".format(one_line))
        #out_fasta.write(align[seqname] + "\n")
