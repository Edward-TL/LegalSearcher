import json

def text_remove_nl(text):
    for line in text:
        limit = len(line) - 1
        n_line = line[:limit]
        line = n_line

    return text

def first_word(sentence):
    char = sentence[0]
    n = 0
    while char != ' ' and n < len(sentence):
        n += 1
        try:
            char = sentence[n]
        except:
        #     print('line', sentence)
        #     print('length', len(sentence))
        #     print('last n', n)
        #     print('last char', char)
            pass
    return sentence[:n]


def articles_name(line, sep='.'):
    char = line[0]
    n = 0
    while char != sep:
        n += 1
        char = line[n]
    return line[:n]

def zeros_maker(int_id, str_len = 3):
    zero_string = '0'*(str_len - len(str(int_id))) + str(int_id)

    return zero_string

def make_article_id(book_id, headline_dict, chapter_dict,artId):
    hl_id = headline_dict['headline_id']
    head_id_str = zeros_maker(hl_id, str_len=2)

    chr_id = chapter_dict['chapter_id']
    chr_id_str = zeros_maker(chr_id)

    art_id = zeros_maker(artId)
    article_id = book_id + head_id_str + chr_id_str + art_id

    return article_id


def build_article_dict(book_id, headline_dict, chapter_dict, line, artId):
    article_name = articles_name(line)
    article_id = make_article_id(book_id, headline_dict, chapter_dict,artId)
    article_dict = {
        'index': "constitucion_politica_de_colombia",
        'id': str.lower(article_id),
        'headline': headline_dict, # head = TITUTLO II, name = de las garantias y los deberes 
        'chapter': chapter_dict, # head = CAPITULO 1, name = de los derechos fundamentales
        'article': {'name': article_name, 'content': [line], 'article_id': article_id},
        # name = Articulo 11, content = El derecho a la vida es inviolable.
        #                               No habra pena de muerte
        }
    return article_dict

def lexical_diversity(article_content):
    flat_text = " "
    flat_text = flat_text.join(article_content)
    return len(flat_text) / len(set(flat_text))

hierarchy = {
    'TITULO' : 'headline',
    'DISPOSICIONES' : 'headline',
    'CAPITULO' : 'chapter',
    'ARTÍCULO' : 'article'

}

def clean_dictionary(or_dictionary, remove_keys={None}, remove_none=False, debugging=False):
    if debugging: print('before cleaning:', or_dictionary)
    '''Mandatory, it removes every None Values.
    Remove_keys is a dictionary in order to remove every key needed in the most
    efficent time'''
    
    if remove_none == True:
        remove_keys.add(None)
    clean_dictionary = {}
    for key, value in or_dictionary.items():
        if debugging: print('cheking value:',value)
        if (key or value) not in remove_keys:
            clean_dictionary[key] = value
            if debugging: print('The new dictionary remains like:', clean_dictionary)
        
        else:
            if debugging: print('Yes, is None, I Know it')
            if debugging: print('The new dictionary remains like:', clean_dictionary)

    if debugging: print('after cleaning:', clean_dictionary)
    return clean_dictionary

def format_articles(articles_list, debugging=False):
    new_art_list = []
    for article in articles_list:
        # First, the things that will remain
        art_id = article['id']
        new_article = {
            'index': article['index'],
            'id': art_id,
        }

        headline_dict = clean_dictionary(article['headline'],remove_keys={'headline_id'},debugging=debugging)
        # headline_json = json.dumps(headline_dict, ensure_ascii=False)
        new_article['headline'] = headline_dict

        chapter_dict = clean_dictionary(article['chapter'],remove_keys={'chapter_id'}, debugging=debugging)
        # chapter_json = json.dumps(chapter_dict, ensure_ascii=False)
        if chapter_dict: new_article['chapter'] = chapter_dict
        
        art_removals = {'article_id', 'lexical_diversity'}
        article_dict = clean_dictionary(article['article'],remove_keys=art_removals,debugging=debugging)
        # article_json = json.dumps(article_dict, ensure_ascii=False)
        new_article['article'] = article_dict

        new_article['embedding'] = article['embedding']
        
        
        new_art_list.append(new_article)
    return new_art_list

def articles_info(book_id, constitution, hierarchy_dict=hierarchy, debugging=True, remove_lineBreak = False):
    article_list = []
    headline, chapter = "", ""
    name_next_headline, name_next_chapter = False, False
    hlId, chId, artId = 0,0,0
    index = 0
    for line in constitution:
        if debugging: print(f"\nIndex: {index} ---------------\n")
        hint = first_word(line).upper()
        
        if remove_lineBreak:
            line = line.rstrip("\n")
        
        if debugging: print(line, 'checking: ', hint)

        if hint in hierarchy_dict: # is a header
            # Which head?
            h = hierarchy_dict[hint]
            if debugging: print('is an ', h)

            # In case the chapter or title (like "Disposiciones") did not have 
            # a name.
            if name_next_headline:
                headline_dict['title'] = headline
                name_next_headline = False

            if name_next_chapter:
                if debugging: print('storing chapter', chapter)
                chapter_dict['title'] = chapter
                name_next_chapter = False

            if h == 'headline':
                if debugging: print('Yeap! headline')
                headline = line
                chId, artId = 0,0
                hlId += 1
                name_next_headline = True
                # All articles belong to a headline, but some doesn't
                # have an chapter. That's why is an trigger.
                # Some titles can start with articles and not chapters
                headline_dict = {'title': headline, 'name': None, 'headline_id': hlId}
                chapter_dict = {'title': None, 'name': None, 'chapter_id':chId}
                

            elif h == 'chapter':
                if debugging: print('Yeap! chapter')
                chapter = line
                chId += 1
                # This line is for creating a new dictionary, not as a call
                chapter_dict = {'title': chapter, 'name': None, 'chapter_id' : chId}
                if debugging: print(chapter_dict)
                
                name_next_chapter = True
            
            else: # article
                if debugging: print('Yeap! article')
                
                artId += 1

                article_data = build_article_dict(book_id, headline_dict, chapter_dict, line, artId)
                if debugging: print(article_data)
                article_list.append(article_data)
        else: #is an article
            if name_next_headline == True:
                headline_dict['name'] = line
                name_next_headline = False
                if debugging: print('headline_dict', headline_dict)
                
            elif name_next_chapter == True:
                chapter_dict['name'] = line
                name_next_chapter = False
                if debugging: print('chapter_dict', chapter_dict)
            
            else:
                article_dict = article_list[-1]
                art_cont = article_dict['article']['content']
                art_cont.append(line)
                article_dict['article']['content'] = art_cont
                if debugging: print(line, 'is not on dict')
        index += 1
    # Enrichment area.
    for art in range(len(article_list)):
        lex_div = lexical_diversity(article_list[art]['article']['content'])
        article_list[art]['article']['lexical_diversity'] = lex_div

    return article_list


ascii_list = ((33,47),(58,64),(91,96),(123,126))
chars = []
for tupple in ascii_list:
    for n in range(tupple[0], tupple[1]):
        chars.append(chr(n))
import re
def clean_words(text, debugging=False):
    
    if debugging: print(text)
    
    join_text = " "
    join_text.join(text)
    if debugging: print(join_text)
    words = re.split(r'\W+', join_text)
    # for char in chars:
    #     text = text.replace(char, '')
    return words

def titles_content(articles_list):
    titles_content = {}
    for article in articles_list:
        title = article['headline']['title']
        if title not in titles_content:
            titles_content[title] = {
                'name': article['headline']['name'],
                'chapters': {},
            }

        title_chapters = titles_content[title]['chapters']
        chapter = article['chapter']['title']

        if chapter not in title_chapters:
            title_chapters = {
                'names' : article['chapter']['name'],
                'avg_lexical_diversity' : None,
                'total_words' : None,
                'total_unique_words' : None,
            }
            titles_content[title]['chapters'][chapter] = title_chapters

        
    return titles_content

# article_dict = {
#     # En caso de que el titulo no tenga nombre, agregara un valor nulo: None
#     'h1':{ 'head': 'TITULO x', 'name': 'Nombre del Titulo'},
#     # En caso de no tener capitulo, agregara en ambos un valor nulo: None
#     'h2':{ 'head': 'CAPITULO x', 'name': 'Nombre del Capitulo'}, 
#     'article':{ 'name': 'Articulo x', 'content': 'Contenido de todo el articulo'},
# }

# legal_document = {
#     # Por ejemplo
#     'name' : 'Constitucion Politica de Colombia',
#     # Podemos agregar mas datos, como:
#     # - fecha de publicacion
#     # - ultima fecha de actualizacion
#     # - pais
#     'content': [article_dict_1, article_dic_2, ..., article_n]
# }


