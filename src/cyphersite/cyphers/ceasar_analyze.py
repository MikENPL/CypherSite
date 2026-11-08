import sys
import getopt
from . import common, ceasar
from enum import Enum

class DecipherMode(Enum):
    BRUTE = 1
    PARTIAL = 2
    CHI = 3
alphabet = common.english
frequencies = common.english_frequencies
def calculate_frequencies(text: str):
    return {i: text.count(i)/len(text) for i in alphabet}

def brute_force(text):
    results = []
    for i in range(len(alphabet)):
        results.append(ceasar.run(text, i))
    return {i: v for i, v in enumerate(results)}

def partial_analysis(text):
    cipher_frequencies = common.sort_dictionary(calculate_frequencies(text)) 
    shifts = []
    expected = sorted(frequencies, key=frequencies.get, reverse=True)
    observed = sorted(cipher_frequencies, key=cipher_frequencies.get, reverse=True)
    for i in range(len(alphabet)):
        shifts.append((alphabet.index(expected[i]) - alphabet.index(observed[i])) % len(alphabet))
    return max(shifts, key=shifts.count)

def chi_analysis(text):
    chi = [0 for _ in range(len(alphabet))]
    for i in range(len(alphabet)):
        cipher_frequencies = calculate_frequencies(ceasar.run(text, i))
        for letter in alphabet:
            chi[i] += ((cipher_frequencies[letter] - frequencies[letter])**2) / frequencies[letter]
    return chi.index(min(chi))

def main():
    opts, args = getopt.gnu_getopt(sys.argv[1:], "bpcf:P")
    filename, mode = None, None
    global alphabet
    global frequencies
    for opt, val in opts:
        if opt == "-b":
            mode = DecipherMode.BRUTE
        elif opt == "-p":
            mode = DecipherMode.PARTIAL
        elif opt == "-c":
            mode = DecipherMode.CHI
        elif opt == "-f":
            filename = val
        elif opt == "-P":
            alphabet = common.polish
            frequencies = common.polish_frequencies

    if filename:
        with open(filename, "r") as file:
            text = file.read().upper()
    else:
        text = " ".join(args).upper()

    match mode:
        case DecipherMode.BRUTE:
            print(brute_force(text))
            exit(0)
        case DecipherMode.PARTIAL:
            key = partial_analysis(text)
        case DecipherMode.CHI:
            key = chi_analysis(text)
        
    print(f"Most likely key is: {key}")
    print(ceasar.run(text, key))

if __name__ == "__main__":
    main()
