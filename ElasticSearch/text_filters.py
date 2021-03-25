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

def get_art_name(line, sep={'.', "," ,";", "-","°", "º"}):
    char = line[0]
    n = 0
    flag = False
    while flag == False and n < len(line):
        char = line[n]
        if char in sep: flag = True
        n += 1

    article_n = line[:n]
    # identifier = article_n.split
    return article_n

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

def text_removals(dot_text):
    ndot_text = []
    index = 0
    for line in dot_text:
    # Step 1: Remove de line breaks "\n.".
        if line == '\n.':
            pass
        elif len(line) == 0:
            pass
        # Step 2:Remove the space at the begging.
        elif  line[0] == ' ':
            ndot_text.append(line[1:])
        # Step 3:Remove the \n for headlines and chapters

        elif line[-1:] == '\n':
            # Some elements are just line breaks, and adding the condition into
            # an "AND" on the if doesn't remove it
            if len(line) > 2:
                ndot_text.append(line.rstrip("\n"))
        # Nothing to change
        else:
            ndot_text.append(line)
        index += 1
    # Step 3: Print the true len of the dot_text.
    print('Total elements:', len(ndot_text), '\n----------------------')

    index = 0

    for line in ndot_text:
        # Step 1: Remove de line breaks "\n.".
        if line == '\n.':
            ndot_text.pop(index)
        index +=1

    return ndot_text