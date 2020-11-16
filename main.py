import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifer(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers = classifiers

    def classify(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        return mode(votes)

    def confidence(self,features):
        votes = []
        for c in self._classifiers():
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes/len(votes)
        return conf


documents = []
for category  in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        documents.append(list((movie_reviews.words(fileid),category)))

random.shuffle(documents)
all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

word_features = list(all_words.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for words in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev),category) for(rev,category) in documents]
training_set = featuresets[:1900]
testing_set = featuresets[1900:]

