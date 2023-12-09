
"""
Name: Katie Schaumleffle
CS 370- Fall 2023
Assignment: Bloom Filters
"""

import argparse
import hashlib
from array import array
import time
# from math import ceil, log, exp, pow

class CountingBloomFilter:
    def __init__(self, size: int, hash_count: int):
        self.size = size
        self.hash_count = hash_count
        # self.calculate_parameters()
        self.bit_array = array('b', [0] * self.size)
        print(f"Size of bit array: {self.size}")

    # def calculate_parameters(self):
    #     self.n = ceil(self.size / (-self.hash_count / log(1 - exp(log(0.01) / self.hash_count))))
    #     self.p = pow(1 - exp(-self.hash_count / (self.size / self.n)), self.hash_count)
    #     self.m = ceil((self.n * log(self.p)) / log(1 / pow(2, log(2))))

    def _hash(self, word, seed):
        hash_object = hashlib.md5(word.encode('utf-8'))
        hash_object.update(seed.to_bytes(4, byteorder='big'))
        return int.from_bytes(hash_object.digest(), byteorder='big') % self.size

    def add_word(self, word):
        for seed in range(self.hash_count):
            index = self._hash(word, seed)
            self.bit_array[index] += 1

    def check_word(self, word):
        for seed in range(self.hash_count):
            index = self._hash(word, seed)
            if self.bit_array[index] == 0:
                return False
        return True

def parse_arguments():
    parser = argparse.ArgumentParser(description='Bloom filter implementation and testing')
    parser.add_argument('input_file', nargs='?', default='rockyou.txt',
                        help='Input file with values to populate the Bloom filter')
    parser.add_argument('test_file', nargs='?', default='dictionary.txt',
                        help='File containing values to be tested')
    parser.add_argument('--bits', type=int, default=134198017,
                        help='Number of bits in the Bloom filter')
    parser.add_argument('--hashes', type=int, default=10,
                        help='Number of hash functions to use')
    return parser.parse_args()

def test_bloom_filter(bloom_instance: CountingBloomFilter, input_file_path, check_file_path):
    filter_set = set()

    try:
        with open(input_file_path, 'r', encoding='ISO-8859-1') as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                filter_set.add(line.strip())
                bloom_instance.add_word(line.strip())
    except FileNotFoundError:
        print("Input file not found.")
    except UnicodeDecodeError:
        print("Error decoding the input file, this program only takes files of ISO-8859-1 type")

    results = {
        'true_neg': 0,
        'false_neg': 0,
        'false_pos': 0,
        'true_pos': 0
    }

    try:
        with open(check_file_path, 'r', encoding='ISO-8859-1') as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                result = bloom_instance.check_word(line.strip())
                if result:
                    if line.strip() in filter_set:
                        results['true_pos'] += 1
                    else:
                        results['false_pos'] += 1
                else:
                    if line.strip() in filter_set:
                        results['false_neg'] += 1
                    else:
                        results['true_neg'] += 1
    except FileNotFoundError:
        print("Check file not found.")
    except UnicodeDecodeError:
        print("Error decoding the test file, this program only takes files of ISO-8859-1 type")

    return results

def print_execution_time(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution Time: {elapsed_time:.4f} seconds")

def main():
    start_time = time.time()
    args = parse_arguments()
    input_file = args.input_file
    test_file = args.test_file

    print("Initiating Bloom Filter...")
    bloom_filter = CountingBloomFilter(args.bits, args.hashes)

    print("Testing Bloom Filter...")
    results = test_bloom_filter(bloom_filter, input_file, test_file)

    total_tested = sum(results.values())
    true_neg = round(results['true_neg'] / total_tested * 100)
    false_neg = round(results['false_neg'] / total_tested * 100)
    false_pos = round(results['false_pos'] / total_tested * 100)
    true_pos = round(results['true_pos'] / total_tested * 100)

    print(f"True negative = {results['true_neg']} words")
    print(f"False negative = {results['false_neg']} words")
    print(f"False positive = {results['false_pos']} words")
    print(f"True positive = {results['true_pos']} words")
    print("The following results are rounded percentages:")
    print(f"True negative: {true_neg}%")
    print(f"False negative: {false_neg}%")
    print(f"False positive: {false_pos}%")
    print(f"True positive: {true_pos}%")
    print(f"Number of hash functions used: {args.hashes}")

    # print(f"Probability of False Positives: {bloom_filter.p:.6f}")

    print_execution_time(start_time)

if __name__ == "__main__":
    main()
