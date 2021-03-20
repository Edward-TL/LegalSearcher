import json
from text_filters import *
from support import *
from objects import *


def make_article_id(book_id, headline_dict, chapter_dict,artId):
    hl_id = headline_dict['headline_id']
    head_id_str = zeros_maker(hl_id, str_len=2)

    chr_id = chapter_dict['chapter_id']
    chr_id_str = zeros_maker(chr_id)

    art_id = zeros_maker(artId)
    article_id = book_id + head_id_str + chr_id_str + art_id

    return article_id

'''build_article_dict(book_id, headers, line, headers['article']['count'])'''
def build_article_dict(code_info, headers_dict, line):
    # articles_name is @ text_filters
    article_name = get_art_name(line)

    article_id = index_hierarchy_id(code_info['id'], headers_dict)
    # print(article_id)
    article_dict = {
        'index': code_info['id'],
        'legal_source' : code_info['source_name'],
        'id': str.lower(article_id),
        }
    for key, key_dictionary in headers_dict.items():
        article_dict[key] = key_dictionary
    # name = Articulo 11, content = El derecho a la vida es inviolable.
    #                               No habra pena de muerte
    article_dict['article'] = {'name': article_name, 'content': [line]}
    return article_dict

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

def format_articles(articles_list, headers_dict, debugging=False):
    new_art_list = []
    for article in articles_list:
        # First, the things that will remain
        new_article = {
            'index': article['index'],
            'legal_source' : article['legal_source'],
            'id': article['id'],
        }

        for key in headers_dict:
            if key != 'article':
                key_dict = clean_dictionary(article[key],remove_keys={'count'},debugging=debugging)
                new_article[key] = key_dict
        
        art_removals = {'article_id'}
        article_dict = clean_dictionary(article['article'],remove_keys=art_removals,debugging=debugging)
        # article_json = json.dumps(article_dict, ensure_ascii=False)
        new_article['article'] = article_dict

        new_article['dot_comma_sep'] = article['dot_comma_sep']
        new_art_list.append(new_article)

    return new_art_list

hierarchy = codes_hierarchy
def start_headers():
    headers_zero = {
    'book': {'title': None, 'name': None, 'count' : 0},
    'part' : {'title': None, 'name': None, 'count' : 0},
    'headline': {'title': None, 'name': None, 'count' : 0},
    'chapter': {'title': None, 'name': None, 'count' : 0},
    'section': {'title': None, 'name': None, 'count' : 0},
    'article' : {'count' : 0},
        }
    return headers_zero

headers = headers



def articles_info(code_info, legal_code, hierarchy_dict=hierarchy, main=None, debugging=True, remove_lineBreak = False):
    article_list = []
    headers = start_headers()
    if main == None:
        main = 'headline'
    
    name_next = False
    index = 0
    for line in legal_code:
        if debugging: print(f"\nIndex: {index} ---------------\n")
        hint = first_word(line).upper()
        
        if remove_lineBreak:
            line = line.rstrip("\n")
        
        if debugging: print(line, 'checking: ', hint)

        if hint in hierarchy_dict: # is a header
            # Which head?
            reference = hierarchy_dict[hint]
            if debugging: print('is an ', reference)

            # The main section that resets the othes but the articles
            if reference == main:
                if debugging: print('Yeap! main:', main)
                headline = line
                for key in headers:
                    if key != main and key != 'article':
                        headers[key] = {'title': None, 'name': None, 'count' : 0}
                name_next = True
                # All articles belong to a headline, but some doesn't
                # have an chapter. That's why is an trigger.
                # Some titles can start with articles and not chapters
                headers[main]['title'] = line
                headers[main]['count'] += 1
            
            # Well, you know... is an article
            elif reference == 'article': 
                if debugging: print("It's article")
                
                headers['article']['count'] += 1

                article_data = build_article_dict(code_info, headers, line)
                if debugging: print_dict_content(article_data,
                                message = "Article's dictionary content:")
                article_list.append(article_data)

            # The rest of the sections
            else:
                if debugging: print('No main, no article, but a section:', reference)
                headers[reference]['title'] = line
                headers[reference]['count'] += 1
                # This line is for creating a new dictionary, not as a call
                
                if debugging: print(headers[reference])
                
                name_next = True

        else: #is the content of an article 
            # or the name of a section
            if name_next == True:
                headers[flag]['name'] = line
                name_next = False
                flag = None
                if debugging: print('main_dict', headers[main])
               
            
            else: #content of the article
                article_dict = article_list[-1]

                # Trial of debugging
                if debugging: print(line, 'is not on dict')
                if debugging: print('index: ', index)
                if debugging: print(article_dict)

                art_cont = article_dict['article']['content']
                art_cont.append(line)
                article_dict['article']['content'] = art_cont

        if name_next: flag = reference
        index += 1

    # Enrichment area.
    # for article in range(len(article_list)):
    #     lex_div = lexical_diversity(article_list[art]['article']['content'])
    #     article_list[art]['article']['lexical_diversity'] = lex_div


    
    # level = {
    #     'book': 6,
    #     'part' : 5,
    #     'headline': 4,
    #     'chapter': 3,
    #     'section': 2,
    #     'article' : 1
    # }
    return article_list


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


