import json


class sentence:
    def __init__(self, data, tfidf, vector, tfidf_val):
        self.tfidf_val = tfidf_val
        self.tfidf = tfidf
        self.vector = vector
        self.data = data

    def toJSON(self):
        jsonobj = {
            "sentence": {
                "data": json.dumps(self.data),
                "tfidf_val": json.dumps(self.tfidf_val),
                "tfidf": json.dumps(self.tfidf),
                "vector": json.dumps(self.vector.tolist()),
            }
        }
        return json.dumps(jsonobj, sort_keys=True, indent=4, separators=(',', ': '))