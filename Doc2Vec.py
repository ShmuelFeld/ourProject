from textblob import TextBlob as tb

import sentence
from TfidfVocabCreator import Tfidf_Creator as TFIDF
import configuration
import encoder_manager
import numpy as np
import document as doc

# Set paths to the model.
VOCAB_FILE = "./data/vocab.txt"
EMBEDDING_MATRIX_FILE = 'use_trained_model'
CHECKPOINT_PATH = "./model/train/model.ckpt-22638"
TEXT_FILE = "/home/shmuelfeld/Desktop/inputFiles_Heb/*.txt"

data = []
tfidf = TFIDF()
tfidf_dict = tfidf.get_tfidf_dic(TEXT_FILE)
encoder = encoder_manager.EncoderManager()
encoder.load_model(configuration.model_config(),
                   vocabulary_file=VOCAB_FILE,
                   embedding_matrix_file=EMBEDDING_MATRIX_FILE,
                   checkpoint_path=CHECKPOINT_PATH)


def sentence_to_vec(sentence):
    sen = list()
    sen.append(sentence)
    return encoder.encode(sen)


def sens2vec(list_of_sentences, total_tfidf):
    multed = []
    for sent in list_of_sentences:
        if total_tfidf == 0:
            total_tfidf += 1
        multed.append(np.dot(sent.tfidf_val/total_tfidf, sent.vector))
    the_vec = sum(multed)
    return the_vec

def create_doc_object(list_of_sentences):
    sentences = []
    total_tfidf = 0
    for sent in list_of_sentences:
        words = tb(sent).words
        tfidf_dic = tfidf.generate_dictionary_for_specific_words(words)
        tfidf_val = tfidf.get_sentence_value(sent)
        vector = sentence_to_vec(sent)
        sentences.append(sentence.sentence(sent, tfidf_dic, vector[0],tfidf_val))
        total_tfidf += tfidf_val
    return doc.documant(sentences, total_tfidf, sens2vec(sentences, total_tfidf))




