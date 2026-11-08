import sys
import getopt
from . import common

alphabet = common.english

def run(text, key, decrypt_flag = False):
    text = list(text)
    key = list(key)
    decrypt_flag = -1 if decrypt_flag else 1

    key_index = 0
    for index, letter in enumerate(text):
        if letter in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            text[index] = alphabet[(alphabet.index(letter) + shift*decrypt_flag) % len(alphabet)]
            key_index += 1
    return ''.join(text)

def main():
    opts, args = getopt.gnu_getopt(sys.argv[1:], "pk:f:d")
    decrypt_flag = False
    key = "" 
    filename = None
    global alphabet
    for opt, val in opts:
        if opt == "-P":
            alphabet = common.polish
        elif opt == "-k":
            key = val.upper()
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
