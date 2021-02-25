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

def build_article_dict(h1_dict, h2_dict, line):
    article_name = articles_name(line)
    article_dict = {
        'h1': h1_dict, # head = TITUTLO II, name = de las garantias y los deberes 
        'h2': h2_dict, # head = CAPITULO 1, name = de los derechos fundamentales
        'article': {'name': article_name, 'content': [line]},
        # name = Articulo 11, content = El derecho a la vida es inviolable.
        #                               No habra pena de muerte
        }
    return article_dict

hierarchy = {
    'TITULO' : 'h1',
    'DISPOSICIONES' : 'h1',
    'CAPITULO' : 'h2',
    'ARTÍCULO' : 'p'

}
def articles_info(constitution, hierarchy_dict=hierarchy, debugging=True):
    article_list = []
    h1, h2 = "", ""
    name_next_h1, name_next_h2 = False, False
    
    for line in constitution:
        hint = first_word(line).upper()
        if debugging: print(hint, 'checking: ', line)

        if hint in hierarchy_dict: # is a header
            # Which head?
            h = hierarchy_dict[hint]
            if debugging: print('is an ', h)

            # In case the chapter or title (like "Disposiciones") did not have 
            # a name.
            if name_next_h1 == True:
                h1_dict = {'head': h1, 'name': None}
                name_next_h1 = False
            if name_next_h2 == True:
                h2_dict = {'head': h2, 'name': None}
                name_next_h2 = False

            if h == 'h1':
                if debugging: print('Yeap! h1')
                h1 = line
                name_next_h1 = True
                # All articles belong to a h1, but some doesn't
                # have an h2. That's why is an trigger.
                # Some titles can start with articles and not chapters
                h2_dict = {'head': None, 'name': None}

            elif h == 'h2':
                if debugging: print('Yeap! h2')
                h2 = line
                name_next_h2 = True
            
            else: # article
                if debugging: print('Yeap! article')

                article_data = build_article_dict(h1_dict, h2_dict, line)
                if debugging: print(article_data)
                article_list.append(article_data)
        else: #is an article
            if name_next_h1 == True:
                h1_dict = {'head': h1, 'name': line}
                name_next_h1 = False
                if debugging: print('h1_dict', h1_dict)
                
            elif name_next_h2 == True:
                h2_dict = {'head': h2, 'name': line}
                name_next_h2 = False
                if debugging: print('h2_dict', h2_dict)
            
            else:
                article_dict = article_list[-1]
                art_cont = article_dict['article']['content']
                art_cont.append(line)
                article_dict['article']['content'] = art_cont
                if debugging: print(line, 'is not on dict')
                

    return article_list

def titles_content(articles_list):
    titles_content = {}
    for article in articles_list:
        title = article['h1']['head']
        if title not in titles_content:
            titles_content[title] = {
                'name': article['h1']['name'],
                'chapters': {},
            }

        title_chapters = titles_content[title]['chapters']
        chapter = article['h2']['head']

        if chapter not in title_chapters:
            title_chapters = {
                'names' : article['h2']['name'],
                'articles' : {},
            }
            titles_content[title]['chapters'][chapter] = title_chapters

        
    return titles_content