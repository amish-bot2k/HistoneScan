#!/usr/bin/env python3
import argparse
import pandas as pd
from Bio import SeqIO

# Function to process the files and fetch sequences
def fetch_sequences(file1_path, file2_path):
    # Read file1 (space-separated)
    file1 = pd.read_csv(file1_path, sep=r"\s+", header=None)
    gene_ids = file1[2].tolist()  # Assuming gene IDs are in column 3

    # Create a dictionary from file2 (FASTA sequences)
    sequences = {}
    for record in SeqIO.parse(file2_path, "fasta"):
        sequences[record.id] = record.seq

    # Fetch sequences from file2 that match gene IDs from file1
    matching_sequences = {gene_id: sequences[gene_id] for gene_id in gene_ids if gene_id in sequences}
    
    # Extract base name of file1 for appending to headers
    file1_name = file1_path.split("/")[-1].split(".")[0]

    # Print the matching sequences to the terminal
    for gene_id, seq in matching_sequences.items():
        print(f">{gene_id}|{file1_name}\n{seq}")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Fetch gene sequences from a FASTA file using gene IDs from a tab-separated file.")
    parser.add_argument("file1", help="Input tab-separated file containing gene IDs")
    parser.add_argument("file2", help="Input FASTA file containing sequences")
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the function to fetch sequences
    fetch_sequences(args.file1, args.file2)

# Run the script if it is executed as the main program
if __name__ == "__main__":
    main()
