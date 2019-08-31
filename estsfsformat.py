import os
import sys

input_vcf = sys.argv[1]
output_est = sys.argv[2]


def get_outgroup_counts(outgroup_0_counts, outgroup_1_counts):
    dic0 = {"A":0, "G":0, "C":0, "T":0}
    dic0[ref_allele] = outgroup_0_counts
    dic0[alt_allele] = outgroup_1_counts
    return ",".join([str(dic0["A"]), str(dic0["G"]), str(dic0["C"]), str(dic0["T"])])

def get_ingroup_counts(ingroup_0_counts, ingroup_1_counts):
    dic1 = {"A":0, "G":0, "C":0, "T":0}
    dic1[ref_allele] = ingroup_0_counts
    dic1[alt_allele] = ingroup_1_counts
    return ",".join([str(dic1["A"]), str(dic1["G"]), str(dic1["C"]), str(dic1["T"])])

with open(input_vcf) as in_vcf:
    with open(output_est, "w") as output_file:
        for line in in_vcf:
            if line[0] != "#":
                x = line.strip("\n").split("\t")
                ref_allele = x[3]
                alt_allele = x[4]
                outgroup_P = x[9]
                outgroup1_genotype = outgroup_P[0]
                outgroup1_0_counts = outgroup1_genotype.count("0")
                outgroup1_1_counts = outgroup1_genotype.count("1")
                outgroup2_genotype = outgroup_P[2]
                outgroup2_0_counts = outgroup2_genotype.count("0")
                outgroup2_1_counts = outgroup2_genotype.count("1")
                out_group1 = get_outgroup_counts(outgroup1_0_counts, outgroup1_1_counts)
                out_group2 = get_outgroup_counts(outgroup2_0_counts, outgroup2_1_counts)
                
                ingroup_0_counts = 0
                ingroup_1_counts = 0
                for a in range(10,44):
                    ingroup_P = x[a]
                    ingroup_genotype = ingroup_P[0:3]
                    ingroup_0_count = ingroup_genotype.count("0")
                    ingroup_1_count = ingroup_genotype.count("1")
                    ingroup_0_counts = ingroup_0_counts + ingroup_0_count
                    ingroup_1_counts = ingroup_1_counts + ingroup_1_count
                
                    in_group = get_ingroup_counts(ingroup_0_counts, ingroup_1_counts)
                output_file.write("{}\t{} {}\n".format(in_group, out_group1, out_group2))


