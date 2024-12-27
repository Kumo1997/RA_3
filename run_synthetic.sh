#!/bin/bash

# Create the results_gen_data and results_2 directories if they don't exist
RESULTS_DIR="results_gen_data"
RESULTS_2_DIR="results_2"
mkdir -p $RESULTS_DIR
mkdir -p $RESULTS_2_DIR

# Loop through different N, n, and alpha values
for N in 5000 10000 15000 20000 25000; do
    for n in 500 1000 2000 2500 3000; do
        for alpha in 0.0 0.5 0.75 1.0 1.5; do
            # Generate the Zipfian data stream using gen_data.py
            OUTPUT_FILE="datastream_N${N}_n${n}_alpha${alpha}.txt"
            echo "Generating data stream with N=$N, n=$n, alpha=$alpha"
            python3 gen_data.py -N $N -n $n -a $alpha -o $OUTPUT_FILE

            # Move the generated file to the results_gen_data directory
            mv $OUTPUT_FILE $RESULTS_DIR/

            # Run the experiment with the generated data stream (main.py)
            RESULT_FILE="results_N${N}_n${n}_alpha${alpha}.txt"
            echo "Running experiment with synthetic data stream ${RESULTS_DIR}/${OUTPUT_FILE}"
            python3.10 main_synthetic.py --txt_file "${RESULTS_DIR}/${OUTPUT_FILE}" --actual_cardinality $n > "${RESULTS_2_DIR}/${RESULT_FILE}"

        done
    done
done
