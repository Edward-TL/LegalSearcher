# import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import numpy as np
import os
import wget
import shutil

root_folder = "LegalSearcher/SentenceEncoder"
embedd_model = f'{root_folder}/model/'
filepath = os.path.abspath(os.path.join('','..', '..',embedd_model))

if os.path.isdir(filepath):
    embed = hub.load(filepath)
else:
    url='https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3?tf-hub-format=compressed'
    fname = wget.download(url) 
    shutil.unpack_archive(fname,'./model')
    embed = hub.load(filepath)
    os.remove('universal-sentence-encoder-multilingual-large_3.tar.gz')
        

##### EMBEDDING #####
def embed_text(text):

    vectors = embed(text)[0].numpy()
    return [vector.tolist() for vector in vectors]
