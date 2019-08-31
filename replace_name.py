#!/usr/bin/env python

fasta= open('Galaxy58-[Extract_Genomic_DNA_on_data_46_and_data_37].fasta')
newnames= open('names_for_fasta_file.txt')
newfasta= open('trial_new_non1.fasta', 'w')

for line in fasta:
    if line.startswith('>'):
        newname= newnames.readline()
        newfasta.write(newname)
    else:
        newfasta.write(line)

fasta.close()
newnames.close()
newfasta.close()
