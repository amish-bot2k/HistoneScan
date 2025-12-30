# Histone protein identification by profile HMM Scan

This repository contains scripts and HMM profiles for identifying and filtering
core histone and CENH3 proteins from proteome or transcriptome-derived protein sets.

## Directory structure

- `bin/` – Python and shell helper scripts
- `HF_lib/` – HMM profiles and Stockholm alignments
- `histone_scan.sh` – Main wrapper script
- `Test_prot.fasta` – Example input protein file

## Requirements
- HMMER (hmmscan)
- Python ≥ 3.7

## Usage
```bash
bash histone_scan.sh Test_prot.fasta

# Histone_scan
