import json

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
          "id: ", article['article']['article_id'],"\n",
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