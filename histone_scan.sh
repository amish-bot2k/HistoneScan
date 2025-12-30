#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SECONDS=0

# ============================================================
# Paths (match your directory layout)
# ============================================================
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bin_dir="${script_dir}/bin"
hmm_dir="${script_dir}/HF_lib"
outdir="${script_dir}/Histone_out"
gid_prefix_list="${bin_dir}/gid_prefix_list"

# ============================================================
# Usage
# ============================================================
usage() {
    echo "Usage: $(basename "$0") <proteome.fasta>"
    exit 1
}

# ============================================================
# Argument & dependency checks
# ============================================================
[[ $# -ne 1 ]] && usage
fasta="$1"

[[ ! -f "$fasta" ]] && {
    echo "ERROR: FASTA file not found: $fasta"
    exit 1
}

# Resolve absolute path for FASTA (important after cd)
fasta_abs="$(cd "$(dirname "$fasta")" && pwd)/$(basename "$fasta")"

command -v hmmscan >/dev/null 2>&1 || {
    echo "ERROR: hmmscan not found. Install HMMER."
    echo "Example: conda install -c bioconda hmmer"
    exit 1
}

# Required Python scripts
py_scripts=(
    compair_and_filter_best_query.py
    fetch_seq.py
    hmmscan_table_seperator.py
    histone_count.py
)

for s in "${py_scripts[@]}"; do
    [[ ! -f "${bin_dir}/${s}" ]] && {
        echo "ERROR: Missing script: ${bin_dir}/${s}"
        exit 1
    }
done

# Required HMM files
hmm_files=(h2a.hmm h2b.hmm h3.hmm h4.hmm cenh3.hmm)
for h in "${hmm_files[@]}"; do
    [[ ! -f "${hmm_dir}/${h}" ]] && {
        echo "ERROR: Missing HMM file: ${hmm_dir}/${h}"
        exit 1
    }
done

[[ ! -f "$gid_prefix_list" ]] && {
    echo "ERROR: gid_prefix_list not found: $gid_prefix_list"
    exit 1
}

# ============================================================
# Run hmmscan
# ============================================================
mkdir -p "$outdir"
echo "Running hmmscan..."

run_hmmscan() {
    local name="$1"
    hmmscan \
        -E 0.0001 \
        --tblout "${outdir}/${name}_hmmscan_all.tblout" \
        "${hmm_dir}/${name}.hmm" "$fasta_abs" \
        > "${outdir}/${name}_hmmsearch.out"
}

for h in h2a h2b h3 h4 cenh3; do
    run_hmmscan "$h"
done

# ============================================================
# Downstream processing
# ============================================================
cd "$outdir"

echo "Merging hmmscan tables..."
cat *_hmmscan_all.tblout > all_hmmscans.tblout

echo "Filtering best hits..."
python3 "${bin_dir}/compair_and_filter_best_query.py" \
    all_hmmscans.tblout all_filtered_hmmscan removed_gids

[[ ! -f all_filtered_hmmscan ]] && {
    echo "ERROR: all_filtered_hmmscan not created"
    exit 1
}

# ============================================================
# Split by histone type + fetch FASTA (SIMPLE LOOP)
# ============================================================
echo "Splitting by histone type and extracting sequences..."

histones=(h2a h2b h3 h4 cenh3)

for h in "${histones[@]}"; do
    gid_file="${outdir}/${h}_gids"
    out_fa="${outdir}/${h}.fa"

    if [[ "$h" == "cenh3" ]]; then
        grep 'CENH3' all_filtered_hmmscan > "$gid_file" || true
    else
        grep "${h}_input" all_filtered_hmmscan > "$gid_file" || true
    fi

    if [[ -s "$gid_file" ]]; then
        echo "  → ${h}: extracting sequences"
        python3 "${bin_dir}/fetch_seq.py" "$gid_file" "$fasta_abs" > "$out_fa"
    else
        echo "  → ${h}: no hits found"
        : > "$out_fa"
    fi
done

# ============================================================
# Done
# ============================================================
duration=$SECONDS
echo "Pipeline completed successfully."
echo "Results directory: $outdir"
echo "Elapsed time: $((duration/60)) min $((duration%60)) sec"
