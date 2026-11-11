import sys, getopt
from cyphersite.ciphers import ceasar_analyze, vigenere
from cyphersite import common
from cyphersite.common import exposed


alphabet = common.english

def kasiski(text: str, kasiski_range, kasiski_sensitivity):
    text = text.upper()
    slices = {} # Slice : array of indexes
    for i in range(len(text)-kasiski_range):
        slice = text[i:i+kasiski_range]
        occurences = text.count(slice)
        indexes = []
        if occurences < kasiski_sensitivity:
            continue
        start = -kasiski_range
        for _ in range(occurences):
            start += kasiski_range + text[start+kasiski_range:].find(slice)
            indexes.append(start)
        slices[slice] = indexes
    return slices

def get_dividers(slices: dict):
    dividers = []
    for indexes in slices.values(): # Calculate distances
        for i in range(len(indexes)-1):
            indexes[i] = indexes[i+1] - indexes[i]
        indexes.pop(len(indexes)-1)

        for j in range(len(indexes)-1): # Common greatest divider
            if indexes[j] > indexes[j+1]:
                a, b = indexes[j], indexes[j+1]
            else:
                a, b = indexes[j+1], indexes[j]
            remainder = None
            while remainder != 0:
                remainder = a % b 
                a, b = b, remainder
            dividers.append(a)

    counted_dividers = {}
    for i in dividers:
        counted_dividers[i] = counted_dividers.get(i, 0) + 1
    counted_dividers = common.sort_dictionary(counted_dividers)

    return [i for i in counted_dividers.keys()]

def coincidence_index(texts: list[str]):
    cis = [0.0 for i in range(len(texts))] # Coincidence IndexeS 
    for i, text in enumerate(texts):
        for letter in alphabet:
            cis[i] += (text.count(letter)*(text.count(letter)-1))
        cis[i] /= len(text)*(len(text)-1)
    print(f"IC dla {len(texts)} kolumn: {cis}")
    return sum(cis)/len(cis)

def column_split(text: str, columns_num: int):
    columns = ["" for i in range(columns_num)]
    text = list(text)
    for i in range(columns_num):
        for j in range(i, len(text), columns_num):
            columns[i] += text[j]
    return columns

@exposed
def run(text: str, kasiski_range: int = 3, kasiski_sensitivity: int = 15):
    text = ''.join(letter for letter in text.upper() if letter in alphabet)
    slices = kasiski(text, kasiski_range, kasiski_sensitivity)
    print(f"Powtarzające się fragmenty: {slices}")
    dividers = get_dividers(slices)
    print(f"Najczęsciej występujące m: {dividers}")
    cis = []
    columns = []
    for i, v in enumerate(dividers):
        columns.append(column_split(text, v))
        cis.append(coincidence_index(columns[i]))
    print(f"Średnie IC dla wszystkich kolumn {cis}")
    ci = max(cis)
    index = cis.index(ci)
    key = ""
    for i in range(dividers[index]):
        key += alphabet[(len(alphabet) - ceasar_analyze.chi_analysis(columns[index][i])) % len(alphabet)]
    return key

def main():
    opts, args = getopt.gnu_getopt(sys.argv[1:], "f:P")
    global alphabet
    filename = None
    for opt, val in opts:
        if opt == "-f":
            filename = val
        elif opt == "-P":
            alphabet = common.polish
        
    if filename:
        with open(filename, "r") as file:
            text = file.read()
    else:
        text = " ".join(args)

    key = run(text)
    print(f"Klucz to {key}\n{vigenere.run(text, key, True)}")

if __name__ == "__main__":
    main()
