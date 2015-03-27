#!/usr/bin/eenv python

import sys

def count_name(filename, protein_name):
    input_file = open(sys.argv[1])
    count = 0
    for line in input_file:
        if line.rstrip() == protein_name:
            count += 1
    return count

if len(sys.argv) != 3:
    sys.exit("Usage: count_name.py <protein names file> <protein name>")

filename = sys.argv[0]
protein_name = sys.argv[1]
name_count = count_name(filename, protein_name)
print protein_name, name_count
