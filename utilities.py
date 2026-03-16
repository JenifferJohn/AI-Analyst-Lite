import hashlib
import time

query_cache = {}

def dataset_hash(df):
    cols = "".join(df.columns)
    return hashlib.md5(cols.encode()).hexdigest()

def cache_get(key):
    return query_cache.get(key)

def cache_store(key,value):
    query_cache[key] = value

class StepLogger:

    def __init__(self):
        self.steps = []
        self.start_time = time.time()

    def log(self,msg):
        timestamp = round(time.time() - self.start_time,3)
        self.steps.append(f"[{timestamp}s] {msg}")

    def engine(self,name):
        self.log(f"Engine used → {name}")

    def timing(self,label,start):
        duration = round(time.time()-start,3)
        self.log(f"{label} completed in {duration}s")

def validate_query(query):

    blocked = [
        "ignore previous instructions",
        "system prompt",
        "jailbreak"
    ]

    for b in blocked:
        if b in query.lower():
            raise ValueError("Unsafe query detected")