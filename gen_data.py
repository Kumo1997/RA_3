import numpy as np
import argparse
import random

def zipfian_distribution(n, alpha):
    """
    Generate the Zipfian probabilities for n elements with parameter alpha.
    """
    ranks = np.arange(1, n + 1) 
    probabilities = 1.0 / np.power(ranks, alpha)
    probabilities /= probabilities.sum()  # Normalize to sum to 1
    return probabilities

def generate_zipfian_data(N, n, alpha):
    """
    Generate a synthetic data stream following a Zipfian distribution.

    Parameters:
    - N: Total length of the data stream.
    - n: Number of distinct elements.
    - alpha: Zipfian parameter controlling skewness.

    Returns:
    - data_stream: List of length N containing elements from 1 to n.
    """
    elements = np.arange(1, n + 1)  # Distinct elements {1, 2, ..., n}
    probabilities = zipfian_distribution(n, alpha)
    data_stream = np.random.choice(elements, size=N, p=probabilities)
    return data_stream

def save_to_file(data_stream, file_path):
    with open(file_path, 'w') as f:
        for element in data_stream:
            f.write(f"{element}\n")
    print(f"Data stream saved to {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Zipfian data stream.")
    parser.add_argument("-N", type=int, required=True, help="Total length of the data stream.")
    parser.add_argument("-n", type=int, required=True, help="Number of distinct elements.")
    parser.add_argument("-a", "--alpha", type=float, default=1.0, help="Zipfian parameter alpha (default: 1.0).")
    parser.add_argument("-o", "--output", type=str, default="datastream.txt", help="Output file name (default: datastream.txt).")

    args = parser.parse_args()
    data_stream = generate_zipfian_data(args.N, args.n, args.alpha)
    save_to_file(data_stream, args.output)
