import math
from textblob import TextBlob as tb
import tensorflow as tens
from pathlib import Path

import Doc2Vec
import sentence
from document import documant

tfs = {}
PATH_TO_DIC = './tfidfvocab.txt'

# create tfidf dictionary
class Tfidf_Creator:
    def __init__(self, input_path = "/home/shmuelfeld/Desktop/inputFiles_Heb/*.txt"):
        self.input_files = input_path
        self.path_to_dic = PATH_TO_DIC
    # return the #word divide by number of words in file
    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)
    # how many files contains thw word
    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)
    # computes "inverse document frequency" which measures how common a word is
    #  among all documents in bloblist
    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))
    # compute tfidf value for word
    def tfidf(self, word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)
    # create string from list of strings for the textblob
    def listToString(self, list):
        ret = ""
        for sent in list:
            ret += sent
        return ret
    # create counter dictionary. how many times each word appears in the files.
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
    # read tfidf dic from file
    def read_dic_from_file(self):
        with open(self.path_to_dic, 'r') as fi:
            for line in fi.readlines():
                li = line.replace('\n','')
                tfs[li.split(':')[0]] = float(li.split(':')[1])
        fi.close()
        return tfs

    # return tfidf dictionary, if the file already exist, so read from the file, else create it
    def get_tfidf_dic(self, input_files_path):
        if Path(self.path_to_dic).is_file():
            return self.read_dic_from_file()
        return self.create_TFIDF_dictionary(input_files_path)

    # create tfidf dictionary file
    def create_TFIDF_dictionary(self,input_files_path):
        pattern = input_files_path
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
        vocab = open('tfidfvocab.txt', 'w+')
        for i, blob in enumerate(bloblist):
            scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
            for score in scores:
                tfs[score] = scores[score]
                # sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                # for word, score in sorted_words[:10]:
                #     print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
            for key, value in tfs.items():
                st = ''
                st += key
                st += ':'
                st += str(value)
                st += '\n'
                vocab.write(st)
        return tfs

    # returns the tfidf value of a given sentence
    def get_sentence_value(self, sentence):
        sentsum = 0
        for word in tb(sentence).words:
            if word in tfs:
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

    def generate_dictionary_for_specific_words(self, words):
        tf_words = {}
        for word in words:
            if word in tfs:
                tf_words[word] = tfs[word]
            else:
                tf_words[word] = 0
        return tf_words


