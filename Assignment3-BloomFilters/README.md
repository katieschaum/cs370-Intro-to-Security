# Bloom Filters

## Author
- **Name:** Katie Schaumleffle
- **Course:** CS 370 - Fall 2023
- **Assignment:** Bloom Filters

## Description
This is a Python implementation of a Bloom Filter. A Bloom Filter is a probabilistic data structure that tests whether a given element is a member of a set. It may return false positives, but no false negatives. The implementation uses counting instead of a binary approach, allowing for removal of items.

## Usage

### Requirements
- Python 3.x
- argparse
- hashlib
- time

### Installation
1. Download the zip file
2. Unzip into a local directory
3. Open and terminal and navigate to the correct directory

### Run the Script
1. Make sure that 'rockyou.txt' and 'dictionary.txt' are located in the same directory as 'schaumlk_bloomfilter.py'. These files should contain the values you want to load into the Bloom filter and test, respectively.
2. Run the script by entering 'python schaumlk_bloomfilter.py' in the terminal
3. *Optional* If you would like to change the input file (rockyou.txt), the test file (dictionary.txt), or the number of bits or hashes run the following command:
    a. python bloom_filter.py [input_file] [test_file] [--bits BITS] [--hashes HASHES]
        -'input_file': Input file with values to populate the Bloom filter (default: 'rockyou.txt').
        -'test_file': File containing values to be tested (default: 'dictionary.txt').
        --bits BITS: Number of bits in the Bloom filter (default: 134198017).
        --hashes HASHES: Number of hash functions to use (default: 10).

### Output
The script will generate a results.txt file that contains the test results. This file lists each word from the dictionary.txt file and its corresponding test result (True Positive, True Negative, False Positive, or False Negative). The script also summarizes the data into a console output of the percentage of each result type after it finishes running.