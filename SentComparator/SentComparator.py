import tensorflow as tf
import numpy as np
from gensim.models import KeyedVectors
import tensorflow_hub as hub
from scipy.spatial.distance import cosine
import os
from scipy.stats import pearsonr
from nltk import tokenize


class SentComparator:
    def __init__(self):
        print('Loading Universal Sentence Encoder...')
        self.embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
        print('Loaded!')

    def loadW2V(self):
        dirname = os.getcwd()
        print('Loading word2vec format')
        w2v = KeyedVectors.load_word2vec_format(os.path.join(dirname, 'GoogleNews-vectors-negative300.bin'),
                                                binary=True)
        print('Loaded')
        return w2v

    def cosine_sim(self, vec1, vec2):
        return 1 - cosine(vec1, vec2)

    def extractW2VSentVector(self, w2v, sent):
        wordvecs = []
        for word in tokenize.word_tokenize(sent):
            if word not in w2v.vocab:
                word = 'UNK'
            wordvecs.append(w2v.word_vec(word))
        return np.mean(np.array(wordvecs), axis=0)

    def evaluateSentSimilarity(self, embed):
        w2v = self.load_w2v()
        f = open('sts-test.csv')
        lines = f.readlines()
        labels, sent1, sent2 = [], [], []

        for line in lines:
            splitline = line.split('\t')
            labels.append(np.float(splitline[4]))
            sent1.append(splitline[5])
            sent2.append(splitline[6])

        predicted = []
        for i in range(len(sent1)):
            predicted.append(self.cosine_sim(self.extractW2VSentVector(w2v, sent1[i]), self.extractW2VSentVector(w2v, sent2[i])))
        print('Average W2V Pearson: ', pearsonr(predicted, labels))
        # Average W2V Pearson:  (0.4029865500760529, 5.4562924625996256e-55)


        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            embed1 = session.run(self.embed(sent1))
            embed2 = session.run(self.embed(sent2))
            predicted = []
            for i in range(len(embed1)):
                predicted.append(self.cosine_sim(embed1[i], embed2[i]))
            print('Universal Sentence Encoder Pearson: ', pearsonr(predicted, labels))
            # Universal Sentence Encoder Pearson:  (0.6747875204778984, 6.702469594372789e-184)

    def compare(self, sent1, sent2):
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            embed1 = session.run(self.embed([sent1]))[0]
            embed2 = session.run(self.embed([sent2]))[0]
            return self.cosine_sim(embed1, embed2)

