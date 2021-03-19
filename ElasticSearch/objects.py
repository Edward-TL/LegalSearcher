'''Everything here is planned to be an object.
The problem now is that the project will be presented
in less than a week. And is easier to call a dictionary
than build and design the objects.'''


# legal_document = {
#     # Por ejemplo
#     'name' : 'Constitucion Politica de Colombia',
#     # Podemos agregar mas datos, como:
#     # - fecha de publicacion
#     # - ultima fecha de actualizacion
#     # - pais
#     'content': [article_dict_1, article_dic_2, ..., article_n]
# }

const_hierarchy = {
    'TITULO' : 'headline',
    'DISPOSICIONES' : 'headline',
    'CAPITULO' : 'chapter',
    'ARTICULO' : 'article'
}

const_headers = {
    'headline': {'title': None, 'name': None, 'count' : 0},
    'chapter': {'title': None, 'name': None, 'count' : 0},
    'article' : {'count' : 0},
}

codes_hierarchy = {
    # Agregados
    'LIBRO': 'book',
    'PARTE': 'part',
    
    # Original
    'TITULO' : 'headline',
    'DISPOSICIONES' : 'headline',
    'CAPITULO' : 'chapter',
    
    # Agregado
    'SECCION': 'section',
    
    #Original
    'ARTICULO' : 'article',
    
    # Agregados
    'CONSIDERANDO' : 'article',
    'PREAMBULO' : 'article',
}

code_info = {
    'main' : None,
    'n_sections': 0,
    'sections': set(),
    'last_section': None,
}


# dont replace it with a simple object, because
# the memory direction will be the same, so any change in one
# will change them all.
headers = {
    'book': {'title': None, 'name': None, 'count' : 0},
    'part' : {'title': None, 'name': None, 'count' : 0},
    'headline': {'title': None, 'name': None, 'count' : 0},
    'chapter': {'title': None, 'name': None, 'count' : 0},
    'section': {'title': None, 'name': None, 'count' : 0},
    'article' : {'count' : 0},
}

level = {
    'book': 6,
    'part' : 5,
    'headline': 4,
    'chapter': 3,
    'section': 2,
    'article' : 1
}