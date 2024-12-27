import randomhash
import math
import os
import re
import sys
import time
import numpy as np
import argparse
from HLL import *
from REC import *

def preprocess_text(file_path):
    """
    Preprocesses the text file by reading and yielding words.
    This function collects all words, including repeated ones.
    """
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            words.append(re.findall(r'\b\w+\b', line.lower()))
    return words

def calculate_standard_deviation(estimates):
    """
    Calculates the standard deviation of the estimates.
    """
    return np.std(estimates)

def theoretical_se_hll(b):
    m = 2 ** b 
    alpha_m = 0.7213 / (1 + 1.079 / m)  # Constant for HyperLogLog
    return alpha_m / np.sqrt(m)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run experiments on data streams.")
    parser.add_argument("--txt_file", type=str, required=True, help="Path to the input TXT file.")
    parser.add_argument("--actual_cardinality", type=int, required=True, help="Actual cardinality (number of distinct elements).")
    args = parser.parse_args()

    file_path = args.txt_file
    actual_cardinality = args.actual_cardinality
    
    # Check if files exist
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    # HyperLogLog and Recordinality setup
    b_values = [8, 10, 12, 14, 16] 
    k_values = [8, 16, 32, 64, 128]
    hll_results = {}
    rec_results = {}

    words = preprocess_text(file_path)

    trials = 10
    rec_estimates = {k: [] for k in k_values}  # Different k values for Recordinality
    rec_times = {k: 0 for k in k_values}  # Time tracking for REC

    # Measure execution time for REC and estimate for different k values
    for trial in range(trials):
        for k in rec_estimates.keys():
            start_time = time.time()
            rec_estimate = recordinality(words, k)
            end_time = time.time()
            rec_estimates[k].append(rec_estimate)
            rec_times[k] += (end_time - start_time)

    avg_rec_estimated_cardinality = {k: sum(rec_estimates[k]) / trials for k in rec_estimates.keys()}
    avg_rec_times = {k: rec_times[k] / trials for k in rec_estimates.keys()}
    
    # Calculate standard deviation for REC
    rec_std_devs = {k: calculate_standard_deviation(rec_estimates[k]) for k in rec_estimates.keys()}

    # HyperLogLog setup - Testing different values of b (counters)
    for b in b_values:
        hll = HyperLogLog(b=b)
        hll_estimated_cardinalities = []
        hll_total_time = 0
        for trial in range(trials):
            hll.buckets = [0] * hll.m
            start_time = time.time()
            for word in words:
                hll.add(word, trial)
            hll_estimated_cardinality = hll.estimate()
            end_time = time.time()
            hll_estimated_cardinalities.append(hll_estimated_cardinality)
            hll_total_time += (end_time - start_time)

        avg_hll_estimated_cardinality = sum(hll_estimated_cardinalities) / trials
        avg_hll_time = hll_total_time / trials

        # Calculate standard deviation for HLL
        std_dev_hll = calculate_standard_deviation(hll_estimated_cardinalities)

        # Store results for different b values in HLL
        hll_results[b] = {
            'avg_estimate': avg_hll_estimated_cardinality,
            'absolute_variation': abs(actual_cardinality - avg_hll_estimated_cardinality),
            'percentage_variation': (abs(actual_cardinality - avg_hll_estimated_cardinality) / actual_cardinality) * 100,
            'execution_time': avg_hll_time,
            'theoretical_se': theoretical_se_hll(b),
            'standard_deviation': std_dev_hll  # Add standard deviation here
        }

    # Print the results for different b values in HLL
    print("\n--- HyperLogLog Results (Varying b) ---")
    for b in hll_results:
        print(f"\nHLL with b={b}:")
        print(f"  Estimated Cardinality: {hll_results[b]['avg_estimate']}")
        print(f"  Absolute Variation: {hll_results[b]['absolute_variation']}")
        print(f"  Standard Deviation: {hll_results[b]['standard_deviation']:.4f}")
        print(f"  Average Execution Time: {hll_results[b]['execution_time']:.4f} seconds")
        print(f"  Theoretical Standard Error: {hll_results[b]['theoretical_se']:.4f}")

    # Store results for REC (same format as HLL)
    print("\n--- Recordinality (REC) Results (Varying k) ---")
    for k in rec_results:
        rec_var = {
            'avg_estimate': avg_rec_estimated_cardinality[k],
            'absolute_variation': abs(actual_cardinality - avg_rec_estimated_cardinality[k]),
            'percentage_variation': (abs(actual_cardinality - avg_rec_estimated_cardinality[k]) / actual_cardinality) * 100,
            'execution_time': avg_rec_times[k],
            'theoretical_se': 1 / np.sqrt(k),  # Theoretical SE for REC
            'standard_deviation': rec_std_devs[k]  # Add standard deviation here
        }

        # Store the results for REC
        rec_results[k] = rec_var

    # Print the results for REC
    for k in rec_results:
        print(f"  \nREC with k={k}:")
        print(f"  Estimated Cardinality: {rec_results[k]['avg_estimate']}")
        print(f"    Absolute Variation: {rec_results[k]['absolute_variation']}")
        print(f"    Standard Deviation: {rec_results[k]['standard_deviation']:.4f}")
        print(f"    Average Execution Time: {rec_results[k]['execution_time']:.4f} seconds")
        print(f"    Theoretical Standard Error: {rec_results[k]['theoretical_se']:.4f}")

    print(f"Actual Cardinality: {actual_cardinality}")
