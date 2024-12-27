import re
import time
import numpy as np
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from HLL import HyperLogLog
from REC import recordinality
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_text(file_path):
    """
    Preprocesses the text file by reading and returning a flat list of words.
    All words are converted to lowercase.
    """
    words = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words.append(re.findall(r'\b\w+\b', line.lower()))  # Use extend instead of append
    return words

def theoretical_se_hll(b):
    m = 2 ** b
    alpha_m = 0.7213 / (1 + 1.079 / m)
    return alpha_m / np.sqrt(m)

def theoretical_se_rec(k):
    return 1 / np.sqrt(k)

def main():
    parser = argparse.ArgumentParser(description="Run experiments on data streams.")
    parser.add_argument("--txt_file", type=str, default="datasets/midsummer-nights-dream.txt", help="Path to the input TXT file.")
    parser.add_argument("--dat_file", type=str, default="datasets/midsummer-nights-dream.dat", help="Path to the input DAT file.")
    args = parser.parse_args()

    txt_file_path = args.txt_file
    dat_file_path = args.dat_file

    words = preprocess_text(txt_file_path)
    distinct_words = preprocess_text(dat_file_path)
    actual_cardinality = len(distinct_words)
    logging.info(f"Actual Cardinality: {actual_cardinality}")

    b_values = [8, 10, 12, 14, 16]
    k_values = [8, 16, 32, 64, 128]
    hll_results = {}
    rec_results = {}

    trials = 5
    rec_estimates = {k: [] for k in k_values}
    rec_times = {k: 0 for k in k_values}

    logging.info("Starting REC experiments...")
    for trial in range(trials):
        for k in rec_estimates.keys():
            seed = trial+1
            start_time = time.time()
            rec_estimate = recordinality(words, k, seed=seed)
            end_time = time.time()
            rec_estimates[k].append(rec_estimate)
            rec_times[k] += (end_time - start_time)
            logging.debug(f"REC Trial {trial + 1}, k={k}: Estimate={rec_estimate}")

    rec_error = {k: [estimate - actual_cardinality for estimate in rec_estimates[k]] for k in rec_estimates.keys()}

    for k in rec_estimates:
        rec_results[k] = {
            'avg_estimate': np.mean(rec_estimates[k]),
            'theoretical_se': theoretical_se_rec(k),
            'execution_time': rec_times[k] / trials,
        }

    logging.info("Starting HyperLogLog experiments...")
    for b in b_values:
        hll_estimated_cardinalities = []
        hll_total_time = 0
        for trial in range(trials):
            hll = HyperLogLog(b=b)
            start_time = time.time()
            for word in words:
                hll.add(word,trial)
            hll_estimated_cardinality = hll.estimate()
            end_time = time.time()
            hll_estimated_cardinalities.append(hll_estimated_cardinality)
            hll_total_time += (end_time - start_time)
            logging.debug(f"HLL Trial {trial + 1}, b={b}: Estimate={hll_estimated_cardinality}")

        hll_error = [estimate - actual_cardinality for estimate in hll_estimated_cardinalities]

        hll_results[b] = {
            'avg_estimate': np.mean(hll_estimated_cardinalities),
            'theoretical_se': theoretical_se_hll(b),
            'execution_time': hll_total_time / trials,
        }

    hll_data = []
    for b in hll_results:
        hll_data.append({
            'b_value': b,
            'hll_avg_estimate': hll_results[b]['avg_estimate'],
            'hll_theoretical_se': hll_results[b]['theoretical_se'],
            'hll_execution_time': hll_results[b]['execution_time'],
            'actual_cardinality': actual_cardinality,
        })

    rec_data = []
    for k in rec_results:
        rec_data.append({
            'k_value': k,
            'rec_avg_estimate': rec_results[k]['avg_estimate'],
            'rec_se': rec_results[k]['theoretical_se'],
            'rec_execution_time': rec_results[k]['execution_time'],
            'actual_cardinality': actual_cardinality,
        })

    hll_df = pd.DataFrame(hll_data)
    rec_df = pd.DataFrame(rec_data)

    try:
        hll_df.to_csv('results_hll.csv', index=False)
        rec_df.to_csv('results_rec.csv', index=False)
        logging.info("Results saved to 'results_hll.csv' and 'results_rec.csv'")
    except Exception as e:
        logging.error(f"Error saving results to CSV: {e}")

    print(f"Actual Cardinality: {actual_cardinality}")
    print("\n--- HyperLogLog Results ---")
    print(hll_df)
    print("\n--- Recordinality (REC) Results ---")
    print(rec_df)

if __name__ == "__main__":
    main()
