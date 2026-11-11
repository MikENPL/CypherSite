import sys
import getopt
from . import ceasar
from enum import Enum

from cyphersite import common
from cyphersite.common import exposed
alphabet = common.english

class DecipherMode(Enum):
    BRUTE = 1
    PARTIAL = 2
    CHI = 3
alphabet = common.english
frequencies = common.english_frequencies
def calculate_frequencies(text: str):
    return {i: text.count(i)/len(text) for i in alphabet}

@exposed
def brute_force(text: str):
    text = text.upper()
    results = []
    for i in range(len(alphabet)):
        results.append(ceasar.run(text, i))
    return {i: v for i, v in enumerate(results)}

@exposed
def partial_analysis(text: str):
    """The key is: """
    text.upper()
    cipher_frequencies = common.sort_dictionary(calculate_frequencies(text)) 
    shifts = []
    expected = sorted(frequencies, key=frequencies.get, reverse=True)
    observed = sorted(cipher_frequencies, key=cipher_frequencies.get, reverse=True)
    for i in range(len(alphabet)):
        shifts.append((alphabet.index(expected[i]) - alphabet.index(observed[i])) % len(alphabet))
    return max(shifts, key=shifts.count)

@exposed
def chi_analysis(text: str):
    """The key is: """
    text.upper()
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
            text = file.read()
    else:
        text = " ".join(args)

    match mode:
        case DecipherMode.BRUTE:
            print(brute_force(text))
            return
        case DecipherMode.PARTIAL:
            key = partial_analysis(text)
        case DecipherMode.CHI:
            key = chi_analysis(text)
        
    print(f"Most likely key is: {key}")
    print(ceasar.run(text, key))

if __name__ == "__main__":
    main()
