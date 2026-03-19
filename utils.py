import hashlib
from difflib import get_close_matches

CACHE = {}

def validate_user_query(query):
    blocked = ["drop", "delete", "--"]
    for b in blocked:
        if b in query.lower():
            raise ValueError("Unsafe query")
    return query

def match_columns(terms, columns):
    mapping = {}
    for t in terms:
        mapping[t] = get_close_matches(t, columns, n=3, cutoff=0.3)
    return mapping

def get_cache_key(q):
    return hashlib.md5(q.encode()).hexdigest()

def get_cached_result(q):
    return CACHE.get(get_cache_key(q))

def set_cache(q, r):
    CACHE[get_cache_key(q)] = r


class Timer:
    import time
    def __init__(self):
        self.start = self.time.time()

    def end(self):
        return round(self.time.time() - self.start, 2)