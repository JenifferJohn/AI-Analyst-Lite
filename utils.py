import time

def validate_user_query(q):
    return q


def safe_response(msg, suggestions=None):
    return {
        "insights": msg,
        "suggestions": suggestions,
        "clarification": True
    }


class StepTimer:
    def __init__(self):
        self.start = time.time()
        self.steps = []

    def log(self, step):
        t = round(time.time() - self.start, 2)
        self.steps.append((step, t))
        return step, t

    def total(self):
        return round(time.time() - self.start, 2)