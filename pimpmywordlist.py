#!/usr/bin/env python
# -------------------------------------------------------------------
# Script feito por zer0-c00L para gerar wordlists com maior grau de
# chance de acerto no momento de auditoria de senhas.
# -------------------------------------------------------------------
#  Revisao: 2017-03-15

import argparse
import itertools
import os
import sys
import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str.encode())
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def log_error(msg):
    print("\033[091mERRO\033[0m: {0}".format(msg))
    return 0

def capitalize(s):
    return s[0:1].upper() + s[1:].lower()

def UpAnDdOwN(s,n=0):
    k = list(s)
    output = ""
    for element in k:
        if k.index(element) % 2 == 0:
            if n is 0:
                output += element.lower()
            else:
                output += element.upper()
        else:
            if n is 0:
                output += element.upper()
            else:
                output += element.lower()
    return output

class PimpMyWordlist(object):
    def __init__(self, file, n):
        self.file = self._open_file(file)
        self._pimp(n)  #  PIMP MA WORDLIST!!!!!

    def _open_file(self, file):
        if not os.path.exists(file):
            log_error("Arquivo nao existe.")
            sys.exit(0)
        return open(file, 'r')

    def _mutate(self, w):
        w = remove_accents(w)
        return [w.lower(), w.upper(), capitalize(w), UpAnDdOwN(w), UpAnDdOwN(w, n=1)]


    def _pimp(self, n):
        charset = list("0987654321_")
        for line in self.file.readlines():
            line = line.replace("\n", "")  # Tira o new line
            for mutated_word in self._mutate(line):
                print(mutated_word)
                for p in itertools.product(charset, repeat=int(n)):
                    print(''.join([mutated_word, ''.join(p)]))
        return 0


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Wordlist a ser pimpada", required=True)
    parser.add_argument("-l", "--length", help="Numero de caracteres concatenados no final de cada palavra", required=True)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    PimpMyWordlist(args.file, args.length)
    return 0

if __name__ == "__main__":
    main()
