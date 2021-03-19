import json
from text_filters import *
from classifier import *
from objects import *

def lexical_diversity(article_content):
    flat_text = " "
    flat_text = flat_text.join(article_content)
    return len(flat_text) / len(set(flat_text))


def print_dict_content(dictionary, message=None):
    if message != None: print(message)
    for key, value in dictionary.items():
        print("     ",key, "=>", value)

# Change it on objects
hierarchy = const_hierarchy

def zeros_maker(int_id, str_len = 3):
    zero_string = '0'*(str_len - len(str(int_id))) + str(int_id)

    return zero_string

def index_hierarchy_id(code_id, headers_dict):

    #     headers = {
    #     'book': {'title': None, 'name': None, 'count' : 0},
    #     'part' : {'title': None, 'name': None, 'count' : 0},
    #     'headline': {'title': None, 'name': None, 'count' : 0},
    #     'chapter': {'title': None, 'name': None, 'count' : 0},
    #     'section': {'title': None, 'name': None, 'count' : 0},
    #     'article' : {'count' : 0},
    #     }
    index_list = [code_id]
    # Yes, i know that this could be made by a for key in headers_dict:
    # But now, the order is of adding is important
    index_list.append( zeros_maker(headers_dict['book']['count'], 2) )
    index_list.append( zeros_maker(headers_dict['part']['count'], 2) )
    index_list.append( zeros_maker(headers_dict['headline']['count'], 2) )
    index_list.append( zeros_maker(headers_dict['chapter']['count'], 2) )
    index_list.append( zeros_maker(headers_dict['section']['count'], 2) )
    index_list.append( zeros_maker(headers_dict['article']['count'], 4) )

    index = ""
    for idx in index_list:
        index += idx
    return index

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
            log_info['message'] = [success_message]
            log_info['error'] = [' ']
    
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

          # "lexical_diversity: ", article['article']['lexical_diversity'],"\n",
    print(f'Article No {art_number+1}: \n',
          "id: ", article['id'],"\n",
          article['headline']['title'],article['headline']['name'],"\n",
          article['chapter']['title'],article['chapter']['name'],"\n",
          article['article']['name'],article['article']['content'])

    print('\n--------------------------------------\n')

def split_text_in_lines(text, delimiter):
    new_text = []
    if delimiter == None:
        print('Missing delimiter value')
        return 

    for paragraph in text:
        if delimiter in paragraph:
            parts = [sentence + delimiter for sentence in paragraph.split(delimiter) if sentence]
            for part in parts:
                new_text.append(part)
        else:
            new_text.append(paragraph)
    text = new_text

    return new_text