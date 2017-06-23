# -*- coding: utf-8 -*-
import nltk

from nltk.corpus import stopwords
from string import punctuation


def is_stop_word(word):
    """Function to check if a word is a Stopword or a punctuation symbol."""
    return word in stopwords.words('english') or word in punctuation


def initialize_nltk_tokenizer():
    """Function to initialize tokenizer from nltk library."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print "Downloading and installing Punkt tokenizer..."
        nltk.download('punkt')
        print "Punkt tokenizer was installed!"


def initialize_nltk_stopwords():
    """Function to initialize stopwords from nltk library."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print "Downloading and installing Stopwords..."
        nltk.download('stopwords')
        print "Stopwords was installed!"
