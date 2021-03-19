# This is juts to set a value and avoid the linting issue
user_query = "Colombia"

simple_query = {
    "query": {
        "simple_query_string": {
            "query": f"{user_query}"
        }
    }
}

query_string = {
    "query": {
        "simple_query_string": {
            "query": f"{user_query}"
        }
    }
}


fuzzy_query = {
    "query": {
        "multi_match" : {
            "query" : "comprihensiv guide",
            "fields": ["title", "summary"],
            "fuzziness": "AUTO"
        }
    },
    "_source": ["title", "summary", "publish_date"],
    "size": 1
}

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


# Like the match_phrase query, it accepts a slop parameter to make the word order
# and relative positions somewhat less rigid
match_phrase_query = {
    "query": {
        "multi_match" : {
            "query": "search engine",
            "fields": ["title", "summary"],
            "type": "phrase",
            "slop": 3
        }
    },
    "_source": [ "title", "summary", "publish_date" ]
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