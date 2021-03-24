# This is juts to set a value and avoid the linting issue
user_query = "Colombia"

class Query:
    def __init__(self, name):
        self.Name = name
    
    def Structure(self, QueryStructure):
        self.Structure = QueryStructure

fields = ['legal_source', 'headline.name', 'section.name','book.name','chapter.name','part.name', 'article.content']

def adapt_queries(user_query):
    Simple = Query(name = 'Simple')
    Simple.Structure(
        {
        "query": {
            "simple_query_string": {
                "query": f"{user_query}"
                }
            }
        }
    )

    # query_string = {
    #     "query": {
    #         "simple_query_string": {
    #             "query": f"{user_query}"
    #         }
    #     }
    # }


    Fuzzy = Query(name = 'Fuzzy')
    Fuzzy.Structure(
        {
        "query": {
            "multi_match" : {
                "query" : f"{user_query}",
                "fields": fields,
                "fuzziness": "AUTO"
            }
        },
        # "_source": ["title", "summary", "publish_date"],
        # "size": 1
        }
    )

    # Like the match_phrase query, it accepts a slop parameter to make the word order
    # and relative positions somewhat less rigid
    MatchPhrase = Query( name = 'Match Phrase')
    MatchPhrase.Structure(
        {
        "query": {
            "multi_match" : {
                "query": f"{user_query}",
                "fields": fields,
                "type": "phrase"#,
                # "slop": 3
            }
        },
        # "_source": [ "title", "summary", "publish_date" ]
        }
    )

    Embedds = Query( name = "Embeddings")
    Embedds.Structure(
        {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'question_vec') + 1.0",
                    "params": {"query_vector": "query_vec"}
                }
            }
        }
        }
    )

    tests = [Simple, Fuzzy, MatchPhrase]

    return tests 

wildcard_query = {
    "query": {
        "wildcard" : {
            "authors" : "t*"
        }
    },
    "_source": ["title", "authors"],
    "highlight": {
        "fields" : {
            "authors" : {}
        }
    }
}

regex_query = {
    "query": {
        "regexp" : {
            "authors" : "t[a-z]*y"
        }
    },
    "_source": ["title", "authors"],
    "highlight": {
        "fields" : {
            "authors" : {}
        }
    }
}


query_string_hl = {
    "query": {
        "query_string" : {
            "query": "(saerch~1 algorithm~1) AND (grant ingersoll)  OR (tom morton)",
            "fields": ["title", "authors" , "summary^2"]
        }
    },
    "_source": [ "title", "summary", "authors" ],
    "highlight": {
        "fields" : {
            "summary" : {}
        }
    }
}