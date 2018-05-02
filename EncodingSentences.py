from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os.path
import scipy.spatial.distance as sd
import configuration
import encoder_manager



# Set paths to the model.
VOCAB_FILE = "./data/vocab.txt"
EMBEDDING_MATRIX_FILE = "/path/to/embeddings.npy"
CHECKPOINT_PATH = "./model/train/model.ckpt-0.data-00000-of-00001"
# The following directory should contain files rt-polarity.neg and
# rt-polarity.pos.
MR_DATA_DIR = "/home/shmuelfeld/Desktop/inputFiles"


# Set up the encoder. Here we are using a single unidirectional model.
# To use a bidirectional model as well, call load_model() again with
# configuration.model_config(bidirectional_encoder=True) and paths to the
# bidirectional model's files. The encoder will use the concatenation of
# all loaded models.
encoder = encoder_manager.EncoderManager()
encoder.load_model(configuration.model_config(),
                   vocabulary_file=VOCAB_FILE,
                   embedding_matrix_file=EMBEDDING_MATRIX_FILE,
                   checkpoint_path=CHECKPOINT_PATH)


# Load the movie review dataset.
# ************************************FOR SHANIIIIIIIIII OTHER COLOR***
# maybe we need to change:
data = []
for filename in os.listdir(MR_DATA_DIR):
    with open(os.path.join(MR_DATA_DIR, filename), 'rb') as f:
        data.extend([line.decode('cp424').strip() for line in f])
# Generate Skip-Thought Vectors for each sentence in the dataset.
encodings = encoder.encode(data)



def get_nn(ind, num=10):
  encoding = encodings[ind]
  scores = sd.cdist([encoding], encodings, "cosine")[0]
  sorted_ids = np.argsort(scores)
  print("Sentence:")
  print("", data[ind])
  print("\nNearest neighbors:")
  for i in range(1, num + 1):
    print(" %d. %s (%.3f)" %
          (i, data[sorted_ids[i]], scores[sorted_ids[i]]))

# Compute nearest neighbors of the first sentence in the dataset.
get_nn(0)



