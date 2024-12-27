import math
import randomhash
import re
import time
from scipy.special import gamma
import os

class HyperLogLog:
    def __init__(self, b=8):
        self.b = b
        self.m = 1 << b  # Number of buckets
        self.buckets = [0] * self.m
        self.alpha_m = self.calculate_alpha_m()

    def calculate_alpha_m(self):
        if self.m == 16:
            return 0.673
        elif self.m == 32:
            return 0.697
        elif self.m == 64:
            return 0.709
        elif self.m >= 128:
            return 0.7213 / (1 + 1.079 / self.m)

    def hash_function(self, word, trial_number):
        # Use high-entropy time-based and random components for unique seed generation
        seed_word = str(trial_number)+ str(word)
        hash_val = randomhash.hash(seed_word)
        return hash_val & ((1 << 128) - 1)

    def trailing_zeros(self, hashed_value):
        binary_representation = bin(hashed_value)[2:]
        reversed_binary = binary_representation[::-1]
        return len(reversed_binary) - len(reversed_binary.lstrip('1'))

    def add(self, word, trial_number):
        hash_val = self.hash_function(word, trial_number)
        idx = hash_val & (self.m - 1)
        leading_zero_count = self.trailing_zeros(hash_val) + 1
        self.buckets[idx] = max(self.buckets[idx], leading_zero_count)

    def estimate(self):
        Z = sum([2 ** -reg for reg in self.buckets])
        E = self.alpha_m * (self.m ** 2) / Z

        # Small range correction (Linear Counting)
        if E < (5 / 2) * self.m:
            V = self.buckets.count(0)
            if V > 0:
                E_star = self.m * math.log(self.m / V)
                return int(E_star)

        # Large range correction (for very large cardinalities)
        if E > (2 ** 32) / 30:
            E_star = -(2 ** 32) * math.log(1 - E / (2 ** 32))
            return int(E_star)

        return int(E)

    def decide_b(self, file_path, epsilon=0.01):
        words = set()
        with open(file_path, 'r') as file:
            for line in file:
                for word in re.findall(r'\b\w+\b', line.lower()):
                    words.add(word)
        
        m = (1.04 / epsilon) ** 2  # m = (1.04 / ε)²
        b = math.ceil(math.log2(m))  # Round up to the nearest integer
        return b

