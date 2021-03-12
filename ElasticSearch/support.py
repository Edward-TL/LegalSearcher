

import re
import json

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


hierarchy = {
    'TITULO' : 'headline',
    'DISPOSICIONES' : 'headline',
    'CAPITULO' : 'chapter',
    'ARTÍCULO' : 'article'
}

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

    # legal_document = {
#     # Por ejemplo
#     'name' : 'Constitucion Politica de Colombia',
#     # Podemos agregar mas datos, como:
#     # - fecha de publicacion
#     # - ultima fecha de actualizacion
#     # - pais
#     'content': [article_dict_1, article_dic_2, ..., article_n]
# }

def add_to_log(log_info, request_response, post_payload):
    response_dict = json.loads(request_response.text)
    payload_id = post_payload['id']
    
    id_list = log_info['id']
    status_list = log_info['status']
    error_list = log_info['error']
    message_list = log_info['message']
    
    # On succes, Elastic Search returns the a info document
    # Whith no status on de text body
    try:
        status = response_dict['statusCode']
    except:
        status = 200
        success_message = 'Success loading the article'
    
    # First Case
    if log_info['id'] == None:
        log_info['id'] = [ post_payload['id'] ]
        
        if status != 200:        
            log_info['status'] = [ response_dict['statusCode'] ]
            log_info['error'] = [ response_dict['error'] ]
            log_info['message'] = [ response_dict['message'] ]
        else:
            log_info['status'] = [ status ]
            log_info['message'] = [' ']
            log_info['error'] = [success_message]
    
    # The rest
    else:
        log_info['id'] = id_list + [payload_id]
        log_info['status'] = status_list + [status]
        

        if status != 200:
            log_info['error'] = error_list + [response_dict['error']]
            log_info['message'] = message_list + [response_dict['message']]
        else:
            log_info['error'] = error_list + [' ']
            log_info['message'] = message_list + [success_message]
        
    return log_info

def print_article(art_number, article):

    print(f'Article No {art_number+1}: \n',
          "id: ", article['article']['article_id'],"\n",
          "lexical_diversity: ", article['article']['lexical_diversity'],"\n",
          article['headline']['title'],article['headline']['name'],"\n",
          article['chapter']['title'],article['chapter']['name'],"\n",
          article['article']['name'],article['article']['content'])

    print('\n--------------------------------------\n')