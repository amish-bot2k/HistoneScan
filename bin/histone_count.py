#!/usr/bin/env python3
import os
import sys
from collections import defaultdict

# Function to count protein occurrences in a plant file
def count_proteins_in_file(file_path):
    protein_counts = {'h2a': 0, 'h2b': 0, 'h3': 0, 'h4': 0,'CENH3': 0}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                gene_id = line.strip()
                # Check for each protein suffix in the gene ID
                if gene_id.startswith('h2a'):
                    protein_counts['h2a'] += 1
                elif gene_id.startswith('h2b'):
                    protein_counts['h2b'] += 1
                elif gene_id.startswith('h3'):
                    protein_counts['h3'] += 1
                elif gene_id.startswith('h4'):
                    protein_counts['h4'] += 1
                elif gene_id.startswith('CENH3'):
                   protein_counts['CENH3'] += 1 
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    return protein_counts

# Get the list of all files in the current directory that end with '_ids.txt'
file_list = [f for f in os.listdir() if f.endswith('_ids.txt')]

# Check if we have any files to process
if not file_list:
    print("No files with '_ids.txt' suffix found.")
    sys.exit(1)

# Prepare a list to store results for each plant
results = []

# Process each plant file found
for file_path in file_list:
    # Extract plant name from file name (assuming file name is the plant name)
    plant_name = os.path.basename(file_path).split('.')[0]  # Remove file extension
    protein_counts = count_proteins_in_file(file_path)
    
    # Add a row for the plant with the protein counts
    results.append([plant_name, protein_counts['h2a'], protein_counts['h2b'], protein_counts['h3'], protein_counts['h4'],protein_counts['CENH3']])

# Print the results in the desired format
print("Plant Name\th2a\th2b\th3\th4\tcenh3")
for row in results:
    print("\t".join(map(str, row)))
