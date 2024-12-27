#!/bin/bash
RESULT_DIR="result_1"
mkdir -p "$RESULT_DIR"

# Iterate through all .txt files in the datasets directory
for txt_file in datasets/*.txt; do
    base_name=$(basename "$txt_file" .txt)

    dat_file="datasets/$base_name.dat"

    if [[ -f "$dat_file" ]]; then
        echo "Processing files: $txt_file and $dat_file"

        result_subdir="$RESULT_DIR/$base_name"
        mkdir -p "$result_subdir"

        python3.10 main.py --txt_file "$txt_file" --dat_file "$dat_file" > "$result_subdir/results.txt"
        echo "Results saved to $result_subdir/results.txt"
    else
        echo "Warning: Matching .dat file for $txt_file not found, skipping."
    fi
done

echo "Processing complete. Results are saved in $RESULT_DIR."
