#!/usr/bin/env python3

"""
Created on Aug 24, 2019 by Yu FENG
Usage: python align_reformat.py -i INPUT -o OUTPUT -f FORMAT
FORMAT : fasta, phylip, nexus

"""

import sys, argparse
import textwrap

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Path for input file")
parser.add_argument("-o", "--output", required=True, help="Path for output file")
parser.add_argument("-f", "--format", required=True, help="Output alignment format")
args = parser.parse_args()
align = {} #define a dictionary


def read_fasta():
    # with open("431146.fasta", "r") as in_fasta:
    seq = ""
    seqname = ""
    seq_num = 0
    for x in line:
    # for line in in_fasta:
        if x[0] == ">":
            seqname = x.strip(">").strip()
            seq_num = seq_num + 1
            seq = ""
        else:
            seq = seq + x.strip()
        align[seqname] = seq
    seq_length = len(seq)
    print("{} sequences detected!".format(str(seq_num)))
    print("Length of alignment is {}!".format(str(seq_length)))
    return align
     
def read_nexus():
    #with open(input, "r") as in_nexus:
    #line = [x.strip() for x in in_nexus]
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
    return align
              
                            
def read_phylip(): 
    # with open(input, "r") as in_phylip:
    #line = [x.strip() for x in input]
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
    return align


def write_fasta():
    with open(output, "w") as out_fasta:
        for seqname in align:
            out_fasta.write(">" + seqname + "\n")
            seq = align[seqname]
            seq_lines = textwrap.wrap(seq, width=50)
            for one_line in seq_lines:
                out_fasta.write("{}\n".format(one_line))
                #out_fasta.write(align[seqname] + "\n")


def write_phylip():
    with open(output, "w") as out_phylip:
        seq_num = len(align)
        seq_length = 0
        part_2 = ""
        #out_phylip.write(" " + str(seq_num) + " " + str(seq_length) + "\n")
        for seqname in align:
            seq = align[seqname]
            seq_length = len(seq)
            seq_lines = textwrap.wrap(seq, width=50, break_on_hyphens=False)
            while len(seqname) <= 11:
                seqname = seqname + " "
            line_one =textwrap.wrap(seq_lines[0], width = 10, break_on_hyphens=False)
            #out_phylip.write(seqname + " ".join(line_one)) + "\n")
            #out_phylip.write(seqname + seq_lines[0] + "\n")
            part_2 = part_2 + seqname + " ".join(line_one) + "\n"
        part_1 = " " + str(seq_num) + " " + str(seq_length) + "\n"
        out_phylip.write(part_1 + part_2)
        
        for i in range(1, len(seq_lines)):
            for seqname in align:
                seq = align[seqname]
                seq_lines = textwrap.wrap(seq, width=50, break_on_hyphens=False)
                out_phylip.write(" ".join(textwrap.wrap(seq_lines[i], width = 10, break_on_hyphens=False)) + "\n")
                # out_phylip.write(seq_lines[i] + "\n")


def write_nexus():
    with open(output, "w") as out_nexus:
        # out_nexus.write("#NEXUS" + "\n")
        # out_nexus.write("BEGIN DATA;" + "\n")
        # out_nexus.write(" DIMENSIONS NTAX=" + str(seq_num) + " NCHAR=" + str(seq_length) + ";\n")
        seq_num = len(align)
        seq_length = 0
        DNA_CHARS = ["A", "G", "T", "C", "-", "?", "N", "a", "g", "t", "c", "n"]
        seq = ""
        NAME = ""
        DATATYPE = ""
        for seqname in align:
            seq = align[seqname]
            for bases in seq:
                if bases in DNA_CHARS:
                    DATATYPE = "DNA"
                #out_nexus.write("FORMAT DATATYPE=DNA INTERLEAVE=yes GAP=-;" + "\n")
                else:
                    DATATYPE = "PROTEIN"
                #out_nexus.write("FORMAT DATATYPE=PROTEIN INTERLEAVE=yes GAP=-;" + "\n")
            seq_length = len(seq)
            seq_lines = textwrap.wrap(seq, width=50, break_on_hyphens=False)
            while len(seqname) <= 9:
                    seqname = seqname + " "
            NAME = NAME + "[Name: " + seqname + "Len: " + str(seq_length) + "]\n"
        INFO1 = "#NEXUS" + "\n" + "BEGIN DATA;" + "\n" + " DIMENSIONS NTAX=" + str(seq_num) + " NCHAR=" + str(seq_length) + ";\n"
        INFO2 = "FORMAT DATATYPE=" + DATATYPE + " INTERLEAVE=yes GAP=-;" + "\n"
        out_nexus.write(INFO1 + INFO2 + NAME)
        out_nexus.write("\nMATRIX\n")
       
        for i in range(0, len(seq_lines)):
            for seqname in align:
                seq = align[seqname]
                seq_lines = textwrap.wrap(seq, width=50, break_on_hyphens=False)
                while len(seqname) <= 10:
                    seqname = seqname + " "
                out_nexus.write(seqname + " ".join(textwrap.wrap(seq_lines[i], width = 10, break_on_hyphens=False)) + "\n")
            out_nexus.write("\n")
        out_nexus.write(";\nEND;\n")
   


if __name__ == "__main__":

    #read input
    with open(args.input, "r") as input:
        line = [x.strip("\n") for x in input]
        if line[0].startswith(">"):
            print("Fasta file detected!")
            align = read_fasta()
        elif line[0].startswith(" "):
            print("Phylip file detected!")
            align = read_phylip()
        elif line[0].startswith("#"):
            print("Nexus file detected!")
            align = read_nexus()
        else:
            print("Unrecognised datatype! Please check your input file!")

    # write output
    output = args.output
    if args.format == "fasta":
        write_fasta()
    elif args.format == "phylip":
        write_phylip()
    elif args.format == "nexus":
        write_nexus()
    else:
        print("Please specify the format you want to transform: fasta, phylip or nexus")
       
        