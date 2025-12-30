#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Usage: python script.py <tblout_file> <prefix_file>")
    sys.exit(1)

# Read command-line arguments
tblout_file = sys.argv[1]
prefix_file = sys.argv[2]

# Step 1: Create a prefix-to-plant mapping from file2
prefix_to_plant = {}
try:
    with open(prefix_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')  # Tab-separated file
        for row in reader:
            if len(row) != 2:
                print(f"Error: Invalid format in {prefix_file}. Each row must have exactly two columns.")
                sys.exit(1)
            prefix, plant = row
            prefix_to_plant[prefix] = plant
except FileNotFoundError:
    print(f"Error: File {prefix_file} not found.")
    sys.exit(1)

# Step 2: Initialize a dictionary to store results for each plant
plant_to_results = defaultdict(list)

# Step 3: Process the HMMER tblout file
try:
    with open(tblout_file, 'r') as f:
        for line in f:
            if line.startswith("#") or not line.strip():  # Skip comments and empty lines
                continue
            columns = line.split()  # Space-separated file
            if len(columns) < 4:
                print(f"Error: Invalid format in {tblout_file}. Each row must have at least four columns.")
                sys.exit(1)
            query_name = columns[0]  # Column 1: query name
            protein_id = columns[2]  # Column 3: protein ID
            e_value = columns[4]     # Column 5: e-value
            # Match the prefix with the mapping
            for prefix, plant in prefix_to_plant.items():
                if protein_id.startswith(prefix):
                    plant_to_results[plant].append(f"{query_name}\t{protein_id}\t{e_value}")
                    break
except FileNotFoundError:
    print(f"Error: File {tblout_file} not found.")
    sys.exit(1)

# Step 4: Write results into separate files for each plant
for plant, results in plant_to_results.items():
    with open(f"{plant}_histone_ids.txt", 'w') as f:
        f.write("\n".join(results))

print("Proteins successfully separated into files with query name and e-value added.")
