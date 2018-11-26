import tensorflow as tf
import numpy as np
from gensim.models import KeyedVectors
import tensorflow_hub as hub
from scipy.spatial.distance import cosine
import os
from scipy.stats import pearsonr
from nltk import tokenize
from statistics import median


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

    def getPearson(self):
        w2v = self.loadW2V()
        labels, sent1, sent2 = self.loadSTS()

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

    # Convert sentence string to Average W2V sentence vector
    def W2VSentence(self, w2v, sent):
        vecs = []
        for word in tokenize.word_tokenize(sent):
            if word in w2v.vocab:
                vec = w2v.word_vec(word)
            else:
                vec = w2v.word_vec('UNK')
            vecs.append(vec)
        return np.mean(np.array(vecs), axis=0)

    def loadSTS(self, binary=False, median=False):
        if median:
            f = open('sts-train.csv', encoding='utf-8')
        else:
            f = open('sts-test.csv', encoding='utf-8')

        lines = f.readlines()
        labels, sent1, sent2 = [], [], []

        for i in range(len(lines)):
            splitline = lines[i].split('\t')
            score = np.float(splitline[4])
            s1 = splitline[5]
            s2 = splitline[6]

            if binary:
                if score >= 4.6:
                    val = 1
                else:
                    val = 0
                labels.append(val)
                sent1.append(s1)
                sent2.append(s2)
            if median:
                if score >= 4.6:
                    sent1.append(s1)
                    sent2.append(s2)
            else:
                labels.append(score)
                sent1.append(s1)
                sent2.append(s2)
        if median:
            return sent1, sent2
        else:
            return labels, sent1, sent2



    # We need to determine at what cosine similarity we deem claims to be equal.
    # Review of the data shows that we generally judge a 4.6 or higher to be equal.
    # Find the median similarity of 4.6+-ranked sentences and use that as our cutoff (median because data is left skewed).
    def FindCutoff(self):
        sent1, sent2 = self.loadSTS(median=True)
        w2v = self.loadW2V()
        sims = []
        for i in range(len(sent1)):
            vec1 = self.W2VSentence(w2v, sent1[i])
            vec2 = self.W2VSentence(w2v, sent2[i])
            sim = self.cosine_sim(vec1, vec2)
            sims.append(sim)
        print('W2V')
        print('Median cosine sim:', median(sims), 'Max:', max(sims), 'Min', min(sims))
        # Median cosine sim: 0.9147900938987732 Max: 1.0 Min 0.4482479989528656

        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            embed1 = session.run(self.embed(sent1))
            embed2 = session.run(self.embed(sent2))
            predicted = []
            for i in range(len(embed1)):
                predicted.append(self.cosine_sim(embed1[i], embed2[i]))
            print('Sentence Encoder')
            print('Median cosine sim:', median(predicted), 'Max:', max(predicted), 'Min', min(predicted))
            # Median cosine sim: 0.8713053166866302 Max: 1.0 Min 0.26762956380844116

    def getPrecisionAndRecall(self):
        labels, sent1, sent2 = self.loadSTS(binary=True)
        w2v = self.loadW2V()
        TP = 0
        FP = 0
        FN = 0
        for i in range(len(sent1)):
            vec1 = self.W2VSentence(w2v, sent1[i])
            vec2 = self.W2VSentence(w2v, sent2[i])
            sim = self.cosine_sim(vec1, vec2)
            if sim >= 0.9147900938987732:
                predict = 1
            else:
                predict = 0
            # print(predict, sim, labels[i], sent1[i], sent2[i])
            if labels[i]:
                if predict:
                    TP += 1
                else:
                    FN += 1
            if predict and not labels[i]:
                FP += 1
        print('W2V')
        print('Precision:', TP / (TP+FP), '\nRecall:', TP/(TP+FN))
        # Precision: 0.5693359375
        # Recall: 0.4096978215038651

        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            embed1 = session.run(self.embed(sent1))
            embed2 = session.run(self.embed(sent2))
            predicted = []
            TP = 0
            FP = 0
            FN = 0
            for i in range(len(embed1)):
                sim = self.cosine_sim(embed1[i], embed2[i])
                if sim >= 0.8713053166866302:
                    predict = 1
                else:
                    predict = 0
                # print(predict, sim, labels[i], sent1[i], sent2[i])
                if labels[i]:
                    if predict:
                        TP += 1
                    else:
                        FN += 1
                if predict and not labels[i]:
                    FP += 1
            print('Sentence Encoder')
            print('Precision:', TP / (TP+FP), '\nRecall:', TP/(TP+FN))
            # Precision: 0.6462962962962963
            # Recall: 0.24525650035137034

    def compare(self, sent1, sent2, w2v=None):
        if w2v:
            v1, v2 = self.W2VSentence(w2v, sent1), self.W2VSentence(w2v, sent2)
            return int(self.cosine_sim(v1, v2) >= 0.9147900938987732)
        else:
            with tf.Session() as session:
                session.run([tf.global_variables_initializer(), tf.tables_initializer()])
                embed1 = session.run(self.embed([sent1]))[0]
                embed2 = session.run(self.embed([sent2]))[0]
                return int(self.cosine_sim(embed1, embed2) >= 0.8713053166866302)

    def batchCompare(self, sent1, sent2, w2v=None):
        if w2v:
            for i in range(len(sent1)):
                v1, v2 = self.W2VSentence(w2v, sent1[i]), self.W2VSentence(w2v, sent2[i])
                if self.cosine_sim(v1, v2) >= 0.9147900938987732:
                    return 1
            return 0

        else:
            with tf.Session() as session:
                session.run([tf.global_variables_initializer(), tf.tables_initializer()])
                embed1 = session.run(self.embed(sent1))
                embed2 = session.run(self.embed(sent2))
                for i in range(len(embed1)):
                    if self.cosine_sim(embed1[i], embed2[i]) >= 0.8713053166866302:
                        return 1
                return 0
    def oneToManyCompare(self, sentences, target, w2v=None):
        if w2v:
            targetv = self.W2VSentence(w2v, target)
            for i in range(len(sentences)):
                v1 = v2 = self.W2VSentence(w2v, sentences[i])
                if self.cosine_sim(v1, targetv) >= 0.9147900938987732:
                    return 1
            return 0

        else:
            with tf.Session() as session:
                session.run([tf.global_variables_initializer(), tf.tables_initializer()])
                embed1 = session.run(self.embed(sentences))
                targete = session.run(self.embed([target]))
                for i in range(len(embed1)):
                    if self.cosine_sim(embed1[i], targete) >= 0.8713053166866302:
                        return 1
                return 0
