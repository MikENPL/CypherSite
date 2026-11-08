import sys
import getopt
from . import common

alphabet = common.english

def run(text, key, decrypt_flag = False):
    text = list(text)
    decrypt_flag = -1 if decrypt_flag else 1

    for index, letter in enumerate(text):
        if letter in alphabet:
            text[index] = alphabet[(alphabet.index(letter) + key*decrypt_flag) % len(alphabet)]

    return ''.join(text)


def main():
    opts, args = getopt.gnu_getopt(sys.argv[1:], "Pk:f:d")
    decrypt_flag = False
    key = 0
    filename = None
    global alphabet
    global frequencies
    for opt, val in opts:
        if opt == "-P":
            alphabet = common.polish
            frequencies = common.polish_frequencies
        elif opt == "-k":
            key = int(val)
        elif opt == "-f":
            filename = val
        elif opt == "-d":
            decrypt_flag = True
        
    if filename:
        with open(filename, "r") as file:
            text = file.read().upper()
    else:
        text = " ".join(args).upper()
        
    print(run(text, key, decrypt_flag))


if __name__ == "__main__":
    main()
