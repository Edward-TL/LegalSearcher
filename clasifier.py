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