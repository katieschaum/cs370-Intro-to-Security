import hashlib as hl
from bitarray import bitarray
from os.path import exists
import time

class BloomFilter:
    def __init__(self, num_bits: int, hash_functions: list):
        self.bits = num_bits
        self.hash_functions = hash_functions
        self.bit_array = self.load_filter("rockyou.txt")

    def load_filter(self, dictionary_file: str = None):
        # Load or create a Bloom filter bit array
        print("BloomFilter::load_filter - Start")
        file_name = f"bitarray_{len(self.hash_functions)}_{self.bits}.txt"
        
        if exists(file_name):
            # Load bit array from disk if it exists
            # print(f"BloomFilter::load_filter - Loading {file_name} from disk")
            bit_array = bitarray()
            print(f"BloomFilter::load_filter - Loading {file_name} from disk with array size {len(bit_array)}")
            with open(file_name, "rb") as file:
                bit_array.fromfile(file)
            print(f"BloomFilter::load_filter - {file_name} loaded successfully")
        else:
            # Create a new bit array and populate it with hashed values from the dictionary
            # print(f"BloomFilter::load_filter - Creating a new bit array")
            bit_array = bitarray(self.bits)
            print(f"BloomFilter::load_filter - Creating a new bit array of size {len(bit_array)}")

            for word in read_file(dictionary_file):
                for hash_func in self.hash_functions:
                    bit = self._get_hash_index(hash_func, word.encode('utf-8'))
                    bit_array[bit] = 1

            # Write the bit array to disk for future use
            with open(file_name, "wb") as file:
                bit_array.tofile(file)

            print(f"BloomFilter::load_filter - {file_name} written to disk")

        print("BloomFilter::load_filter - Complete")
        print(f"BloomFilter total values: {bit_array.count()} of {len(bit_array)}")
        self.print_ba_distribution(bit_array)
        return bit_array

    def _get_hash_index(self, hash_function, word: bytes):
        # Get the hash index for a given word using the specified hash function
        working_hash_function = hash_function.copy()
        working_hash_function.update(word)

        hash_digest = (
            working_hash_function.digest(16)
            if "shake_" in working_hash_function.name
            else working_hash_function.digest()
        )
        return int.from_bytes(hash_digest, "big") % self.bits

    def test_filter(self, test_words: list, master_set: set):
        # Test the Bloom filter against a set of words and calculate statistics
        print("BloomFilter::test_filter")
        positive_words = [word for word in test_words if self.is_positive(word, master_set)]
        negative_words = [word for word in test_words if not self.is_positive(word, master_set)]

        print(f"positive_words: {len(positive_words)} negative_words: {len(negative_words)}")

        false_positives, false_negatives, true_negatives, true_positives = self.calculate_statistics(positive_words, negative_words, master_set)

        print(f"false positives: {len(false_positives)}")
        print(f"false negatives: {len(false_negatives)}")
        print(f"true positives: {len(true_positives)}")
        print(f"true negatives: {len(true_negatives)}")

    def is_positive(self, word, master_set):
        # Check if a word is classified as positive by the Bloom filter
        return all(self.bit_array[self._get_hash_index(hash_func, word.encode('utf-8'))] for hash_func in self.hash_functions)

    def calculate_statistics(self, positive_words, negative_words, master_set):
        # Calculate statistics based on test results
        false_positives = set(positive_words) - master_set
        false_negatives = set(negative_words).intersection(master_set)
        true_negatives = set(negative_words) - master_set
        true_positives = set(positive_words).intersection(master_set)
        return false_positives, false_negatives, true_negatives, true_positives

    def print_ba_distribution(self, bit_array):
        # Print the distribution of values in the Bloom filter bit array
        print(f"BloomFilter Distribution")
        for i in range(20):
            start = i * (len(bit_array) // 20)
            end = (i + 1) * (len(bit_array) // 20)
            print(
                f"{i}: {bit_array[start: end].count()} of {len(bit_array)}: {(bit_array[start: end].count() / bit_array.count()):.4f}"
            )

def read_file(file_name: str, encoding: str = 'latin-1') -> list:
    # Read a file and return a list of words
    with open(file_name, "rb") as file:
        dictionary = file.read().split(b'\n')

    return [word.decode(encoding) for word in dictionary]

def hash_functions(num_functions: int = None):
    # Generate a list of hash functions
    hash_functions = [
        hl.md5(),
        hl.sha3_224(),
        hl.sha3_512(),
        hl.sha3_256(),
        hl.sha1(),
        hl.shake_256(),
        hl.shake_128(),
        hl.blake2s(),
    ]
    return hash_functions[:num_functions] if num_functions else hash_functions

def fp_five_percent():
    # Return params for Bloom filter with 5% false positive rate
    return (89_440_499, hash_functions(4))

def fp_one_percent():
    # Return params for Bloom filter with 1% false positive rate
    return (137_491_831, hash_functions(7))

# def fp_half_percent():
#     # Return params for Bloom filter with 0.5% false positive rate
#     return (158_186_414, hash_functions(8))

def fp_tenth_percent():
    # Return params for Bloom filter with 0.1% false positive rate
    return (206_237_746, hash_functions(10))

def print_execution_time(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution Time: {elapsed_time: .4f} seconds")

def main():
    # Record start time
    start_time = time.time()
    # Main function to test Bloom filters with different params
    filter_params = [fp_five_percent, fp_one_percent, fp_tenth_percent]

    rockyou = read_file("rockyou.txt")
    test_words = read_file("dictionary.txt", encoding="latin-1")

    print(f"Bloom filter length: {len(rockyou)}")
    print(f"Test words length: {len(test_words)}")

    for param in filter_params:
        bloom_filter = BloomFilter(*param())
        bloom_filter.test_filter(test_words, set(rockyou))
    
    print_execution_time(start_time)

if __name__ == "__main__":
    main()