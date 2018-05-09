import math
from textblob import TextBlob as tb
import tensorflow as tens
import json
tfs = {}
class Tfidf_Creator:
    def __init__(self, input_path = "/home/shmuelfeld/Desktop/inputFiles_Heb/*.txt"):
        self.input_files = input_path

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tfidf(self, word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)

    def listToString(self, list):
        ret = ""
        for sent in list:
            ret += sent
        return ret

    def create_counter(self):
        pattern = self.input_files
        input_files = []
        unique_words = []
        match = tens.gfile.Glob(pattern)
        if not match:
            raise ValueError("Found no files matching %s" % pattern)
        input_files.extend(match)
        for file in input_files:
            with open(file, 'r') as fi:
                unique_words.extend(set(tb(self.listToString(fi.readlines())).words))
            fi.close()
        se = set(unique_words)
        dic = {}
        for word in se:
            num = 0
            dic[word] = num

        for file in input_files:
            with open(file, 'r') as fi:
                se = tb(self.listToString(fi.readlines()))
                for word in set(se.words):
                    dic[word] += se.word_counts[word]
            fi.close()
        with open('counterVoceb.txt', 'w') as file:
            for word in dic:
                st = word
                st += " : "
                st += str(dic[word])
                st += '\n'
                file.write(st)
        file.close()

    def create_TFIDF_dictionary(self):
        pattern = self.input_files
        input_files = []
        match = tens.gfile.Glob(pattern)
        if not match:
            raise ValueError("Found no files matching %s" % pattern)
        input_files.extend(match)
        bloblist = []
        for file in input_files:
            with open(file, 'r') as fi:
                bloblist.append(tb(self.listToString(fi.readlines())))
            fi.close()
        for i, blob in enumerate(bloblist):
            print("Top words in document {}".format(i + 1))
            scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
            for score in scores:
                tfs[score] = scores[score]
                # sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                # for word, score in sorted_words[:10]:
                #     print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
        return tfs

    def get_sentence_value(self, sentence):
        sentsum = 0
        for word in tb(sentence).words:
            sentsum += tfs[word]
        return sentsum
    def get_document_value(self, lst):
        docsum = 0
        for sentence in lst:
            docsum += self.get_sentence_value(sentence)
        return docsum
    def get_vector_values(self, lst):
        tfidfvec =list()
        for sen in lst:
            tfidfvec.append(self.get_sentence_value(sen))
        return tfidfvec
