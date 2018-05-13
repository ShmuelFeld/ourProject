import json
import numpy as np

class documant:
    def __init__(self, sentences, tfidf_val, vector):
        self.sentences = sentences    #[] #empty ist of sentence.
        self.tfidf_val = tfidf_val    #0
        self.vector = vector

    def toJSON(self):
        jsonobj = {
            'sentences': [],
            'tfidf_val': self.tfidf_val,
            'vector': json.dumps(self.vector.tolist())
        }

        for s in self.sentences:
            jsonobj['sentences'].append(s.toJSON())
        return json.dumps(jsonobj, sort_keys=True, indent=4, separators=(',', ': '))
