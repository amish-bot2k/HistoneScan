#!/usr/bin/env python3
import pandas as pd
import sys
import os

def process_hmmscan_table(input_file, best_output_file, worst_output_file):
    # Read the input file
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            # Skip comment lines
            if line.startswith('#'):
                continue
            # Split columns using multiple spaces (\s+)
            data.append(line.strip().split())

    # Convert to a DataFrame
    df = pd.DataFrame(data)
    # Assign column names for clarity
    column_count = df.shape[1]
    column_names = [f"Col{i+1}" for i in range(column_count)]
    df.columns = column_names

    # Rename important columns for easier handling
    df.rename(columns={"Col1": "HMM_Name", "Col3": "Gene_ID", "Col5": "E_value"}, inplace=True)
    df["E_value"] = df["E_value"].astype(float)  # Convert E_value to float

    # Find the rows with the best e-values for each Gene_ID
    best_df = df.loc[df.groupby("Gene_ID")["E_value"].idxmin()]
    
    # Identify rows to exclude from best_df
    worst_df = df[~df.index.isin(best_df.index)]

    # Save the results
    best_df.to_csv(best_output_file, sep='\t', index=False, header=False)
    worst_df.to_csv(worst_output_file, sep='\t', index=False, header=False)

    print(f"Best e-value data saved to: {best_output_file}")
    print(f"Removed data saved to: {worst_output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <best_output_file> <worst_output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    best_output_file = sys.argv[2]
    worst_output_file = sys.argv[3]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    process_hmmscan_table(input_file, best_output_file, worst_output_file)
