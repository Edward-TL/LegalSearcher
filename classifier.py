def text_remove_nl(text):
    for line in text:
        limit = len(line) - 1
        n_line = line[:limit]
        line = n_line

    return text
    
def label_dict(name_importance):
    if name_importance == True:
        label_dict = {'name' : None, 'content': None}
    else:
        label_dict = {'content': None}

    return label_dict

def join_labels(text, label, name_importance=True):
    labeled_text = {}
    
    # Intialized the variable
    name_next = False
    
    for n in range(len(text)):
        line = text[n]
        # In all cases, the 0 is an start (also in chapters)
        if n == 0:
            # In case of articles, it does not add the name part
            labeled_text[line] = label_dict(name_importance)
            # Where it remembers the last label used
            last_label = line
            #In other case, this remains as False
            if name_importance == True: name_next = True
                
        else:  # For the next cases
            # Recognize for a new label
            if line[:len(label)].upper() == label.upper():
                # Creates the label on the dictionary
                labeled_text[line] = label_dict(name_importance)
                
                # Remembers the new label
                last_label = line
                if name_importance == True: name_next = True
                    
            else:
                if name_importance == True and name_next == True:
                    # In case that the name matters, like tittles and chapters
                    labeled_text[last_label]['name'] = line
                    
                    name_next = False
                else:
                    if labeled_text[last_label]['content'] == None:
                        labeled_text[last_label]['content'] = [line]
                    else:
                        labeled_text[last_label]['content'].append(line)

    return labeled_text



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
        # head = TITUTLO II, name = de las garantias y los deberes
        'h1': h1_dict, 
        # head = CAPITULO 1, name = de los derechos fundamentales
        'h2': h2_dict,
        # name = Articulo 11, content = El derecho a la vida es inviolable.
        #                               No habra pena de muerte
        'article': {'name': article_name, 'content': [line]},
        }
    return article_dict

jerarquy = {
    'TITULO' : 'h1',
    'DISPOSICIONES' : 'h1',
    'CAPITULO' : 'h2',
    'ARTÍCULO' : 'p'

}
def articles_info(constitution, jerarquy_dict=jerarquy, debugging=True):
    article_list = []
    h1, h2 = "", ""
    name_next_h1, name_next_h2 = False, False
    
    for line in constitution:
        hint = first_word(line).upper()
        if debugging: print(hint, 'checking: ', line)

        if hint in jerarquy_dict: # is a header
            # Which head?
            h = jerarquy_dict[hint]
            if debugging: print('is an ', h)

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