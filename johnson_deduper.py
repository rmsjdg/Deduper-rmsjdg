#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program that removes PCR duplicate reads from a sorted and uniquely-aligned SAM file, returning another SAM file.")
    parser.add_argument("-f", "--file", help="Absolute file path to a sorted and uniquely-aligned SAM file.", required = True, type = str)
    parser.add_argument("-o", "--outfile", help="Desired absolute file path for output file.", required = True, type = str)
    parser.add_argument("-u", "--umi", help="Absolute file path to a list of known UMIs to be found in SAM file.", required = True, type = str)
    return parser.parse_args()
args = get_args()

infile  = args.file
outfile = args.outfile
umifile = args.umi


def stsp(the_line: str) -> list: 
    '''Applies strip and split by tab to a string and returns the result, typically as a list.'''
    return the_line.strip().split("\t")

def find_chr(the_list: list) -> str:
    '''When given a list of elements from a sam file line, returns the chromosome as a string.'''
    return the_list[2]

def is_revcomp(the_list: list) -> bool:
    '''When given a list of elements from a sam file line, returns a bool indicating True if the read came from a reverse complemented strand '''
    flag = int(the_list[1])
    return ((flag & 16) == 16) # Return true if bit 16 is set, which indicates it is a rev_comp (minus) strand.

def find_umi(the_list: list) -> int:
    '''When given a list of elements from a sam file line, returns the umi (taken from the qname) as an int. If no umi is found, returns zero.'''
    umi = the_list[0][-8:] # qname is first element. grab last 8 characters 
    if umi.isalpha():
        return umi
    else:
        return 0

def find_pos(the_list: list, minus: bool) -> int:
    ''' When given a line from a sam file, takes the position, corrects for soft clipping, and returns the "true" 1-based left-most starting position.'''
    pos_initial = int(the_list[3]) # identify initial position
    cigar_list = re.findall(r'(\d+)([A-Z=])', the_list[5]) # run regex on the cigar string to return a list of tuples
    adjust = 0 

    if minus: # minus strand
        if "S" in cigar_list[-1]: # if there is a trailing S
            adjust += int(cigar_list[-1][0])
        for pair in cigar_list: 
            if "M" in pair or "D" in pair or "N" in pair or "X" in pair or "=" in pair: # add any non-clipping adjustment values, except Insertions since they consume query
                adjust += int(pair[0])
        return pos_initial + adjust -1

    else:  # plus strand
        if "S" in cigar_list[0]: # if there is a leading S and we're on the plus strand, subtract softclipping from position
            adjust += int(cigar_list[0][0])
        return pos_initial - adjust


# Initialize set for holding 96 known umis and populate from umi file
umi_set = set()
with open(umifile) as fh_umi:
    for line in fh_umi:
        if line.strip() not in umi_set:
            umi_set.add(line.strip())
        else:
            pass

# Open files 
with open(infile, "rt") as fh_in:
    with open(outfile, "wt") as fh_out:
        # initialize counters 
        header_lines: int = 0
        current_chr = 0 # didnt flag as an int since it may be assigned x, y, etc.
        unique_reads: int = 0
        duplicate_reads: int = 0
        wrong_umis: int = 0
        chr_set: set = set()
        while True:
            line = fh_in.readline()
            # end of file
            if line == "": 
                break
            # header line
            elif line[0] == "@":
                header_lines += 1
                fh_out.write(f"{line}")
            # actual read line
            else:
                linechunks = stsp(line)                 # split the line
                chr = find_chr(linechunks)              # define chromosome
                minus = is_revcomp(linechunks)          # define strand
                umi = find_umi(linechunks)              # define umi
                pos = find_pos(linechunks, minus)   # find position adjustment value
                code = (f"{umi} {pos} {minus}") 

                if umi not in umi_set: # if the umi is unknown, do not write out to file (continue to next line)
                    wrong_umis += 1
                    continue

                if chr != current_chr: # reset dict when reaching new chromosome
                    current_chr = chr
                    chr_set.clear()

                if code not in chr_set:
                    unique_reads += 1
                    chr_set.add(code)
                    fh_out.write(line.strip())
                    fh_out.write("\n")

                else:
                    duplicate_reads += 1
                    pass

print(f"\nHeader lines: {header_lines}\n\
Unique Reads: {unique_reads}\n\
Invalid UMIs: {wrong_umis}\n\
Duplicates Removed: {duplicate_reads}\n\n\
Thank you for using johnson_deduper.py -- Have a nice day!\n")