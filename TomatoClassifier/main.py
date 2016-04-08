from common import load_non_preprocessed_data, load_preprocessed_data, load_preprocessed_2_data
from classifiers import ClassifierOvOFeaturesReduction
from preprocess_2 import filter_feature_sets
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn.cross_validation import StratifiedKFold
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import fit_ovo
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import nltk
import numpy
import os

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

valid_classifiers = {
    "linearsvc": LinearSVC,
    "sgd": SGDClassifier,
    "svc": SVC,
    "voting": VotingClassifier,
}

def main(classifier_name,
         classifier_args=None,
         ngram=2,
         folds=3,
         preprocessed=False
         ):
  if preprocessed:
    X, y = load_preprocessed_data()
  else:
    X, y = load_non_preprocessed_data()

  # StratifiedKFold makes sure that there's no unfortunate data split
  skf = StratifiedKFold(y, folds)

  ###############################
  # Training and testing models #
  ###############################

  print()
  print('training classifier')
  if classifier_args is None:
    classifier_args = {}
  classifier = valid_classifiers[classifier_name](**classifier_args)

  params = {
            "tfidf__ngram_range": [(1, 2)],
            # "Classifier__class_weight": [{ 0: 1, 1: 100, 2: 1}, { 0: 1, 1: 1, 2: 1}],
            # "Classifier__C": [.01, .1, 1, 10, 100],
            # "Classifier__kernel": ['rbf', 'linear', 'poly', 'sigmoid'],
            # "Classifier__penalty": ['l1', 'l2', 'elasticnet'],
            # "Classifier__loss" : ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'],
          }
  ml_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(sublinear_tf=True)),
                    # ('Vectorization', CountVectorizer(binary='false')),
                    # ('Feature Refinement', TfidfTransformer(use_idf=False)),
                    # ('Feature Selection', SelectKBest(chi2, 100)),
                    # ('Feature Reduction', ClassifierOvOFeaturesReduction()),
                    ('Classifier', classifier),
                    ])

  gs = GridSearchCV(ml_pipeline, params, cv = folds, verbose=2, n_jobs=-1)
  gs.fit(X, y)
  print(gs.best_params_)
  print(gs.best_score_)
  print('>>>>>>>>>>')
  print(gs.grid_scores_)

if __name__ == '__main__':
  # classifier_name = "svc"
  # classifier_args = {'C': 1, 'kernel': 'linear'}

  # classifier_name = "sgd"
  # classifier_args = { 'loss': 'log', 'penalty': 'elasticnet' } 

  # classifier_name = "linearsvc"
  # classifier_args = { 'C': 1 } #{ "class_weight": { 0: 1, 1: 100, 2: 1} }

  # classifier_name = "voting"
  # classifier_args = {
  #   "estimators": [
  #       ('sgd', valid_classifiers['sgd'](loss='log', penalty='elasticnet')),
  #       ('svc', valid_classifiers['svc'](C=10, kernel='linear')),
  #       ('svc', valid_classifiers['svc'](C=1, kernel='linear')),
  #       ('svc', valid_classifiers['svc']()),
  #       ('linearsvc', valid_classifiers['linearsvc'](C=10)),
  #       ('linearsvc', valid_classifiers['linearsvc'](C=1))
  #     ]
  # }

  if 'classifier_name' not in locals() or 'classifier_args' not in locals():
    print('Please uncomment a classifier')
    import sys
    sys.exit()

  print('=======================================')
  print(classifier_name)
  print('=======================================')

  main(classifier_name, classifier_args, preprocessed = False, ngram=2)

