
from TfidfVocabCreator import Tfidf_Creator as TFIDF
import configuration
import encoder_manager
import numpy as np


# Set paths to the model.
VOCAB_FILE = "./data/vocab.txt"
EMBEDDING_MATRIX_FILE = 'use_trained_model'
CHECKPOINT_PATH = "./model/train/model.ckpt-22638"
TEXT_FILE = "/home/shmuelfeld/Desktop/inputFiles_Heb/2505_20171206_124724.txt"

data = []
tfidf = TFIDF()
tfidf_dict = tfidf.create_TFIDF_dictionary()
encoder = encoder_manager.EncoderManager()
encoder.load_model(configuration.model_config(),
                   vocabulary_file=VOCAB_FILE,
                   embedding_matrix_file=EMBEDDING_MATRIX_FILE,
                   checkpoint_path=CHECKPOINT_PATH)

def sentence_to_vec(sentence):
    sen = list()
    sen.append(sentence)
    return encoder.encode(sen)

def doc2vec(path):
    with open(path, 'r') as fi:
        vec = sens2vec(fi.readlines())
    fi.close()
    return vec

def sens2vec(lst):
    vecs = encoder.encode(lst)
    doc_val = tfidf.get_document_value(lst)
    tfidfs = tfidf.get_vector_values(lst)
    mult_by_scalar = []
    for i in range(0, len(vecs)):
        mult_by_scalar.append(np.dot(vecs[i]/doc_val, tfidfs[i]))
    the_vec = sum(mult_by_scalar)
    return the_vec




