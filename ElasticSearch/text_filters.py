import re
from unicodedata import normalize

def standarize(word):
    word = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", word), 0, re.I
        )

    # -> NFC
    word = normalize( 'NFC', word)
    
    return word

def first_word(sentence):
    char = ""
    n = 0
    # agregar regex de a-z
    while char != ' ' and n < len(sentence):
        char = sentence[n]
        n += 1

    word = sentence[:n-1]
    # -> NFD y eliminar diacríticos
    word = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
        r"\1", 
        normalize( "NFD", word), 0, re.I
    )
    # -> NFC
    word_normalized = normalize( 'NFC', word)

    return word_normalized

def articles_name(line, sep='.'):
    char = line[0]
    n = 0
    while char != sep:
        n += 1
        char = line[n]
    return line[:n]

ascii_list = ((33,47),(58,64),(91,96),(123,126))
chars = []
for tupple in ascii_list:
    for n in range(tupple[0], tupple[1]):
        chars.append(chr(n))

def clean_words(text, remove_digits=False, debugging=False):
    '''Remove all puntuaction marks using the ascii table.
    The digits from 0 to 9 remains unless that it'is required.
    http://www.asciitable.com/'''

    if debugging: print(text)
    
    join_text = " "
    join_text.join(text)
    if debugging: print(join_text)
    
    words = re.split(r'\W+', join_text)
    if remove_digits:
        words = re.split(r'\b\d+\b', join_text)
    # for char in chars:
    #     text = text.replace(char, '')
    return words