# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import word_tokenize
from utils import is_stop_word, initialize_nltk_tokenizer, initialize_nltk_stopwords


class BooleanModelInformationRetrieval(object):

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, files_path=[]):
        if not files_path:
            raise Exception("No file path was passed!")

        self.files_path = files_path

        initialize_nltk_tokenizer()
        initialize_nltk_stopwords()

        self._generate_vocabulary()
        self._generate_binary_incidence_matrix()

    ###################
    # PRIVATE METHODS #
    ###################

    def _generate_vocabulary(self):
        """Method to generate the BooleanModel vocabulary."""
        self.vocabulary = []

        for path in self.files_path:
            file_ = open(path, "r")
            file_content = " ".join(file_.readlines()).lower()

            for word in word_tokenize(file_content):
                if not is_stop_word(word) and word not in self.vocabulary:
                    self.vocabulary.append(word)

            file_.close()

    def _generate_binary_incidence_matrix(self):
        """Method to generate a binary terms-documents incidence matrix."""
        self.binary_incidence_matrix = {}

        for path in self.files_path:
            file_ = open(path, "r")
            file_content = " ".join(file_.readlines()).lower()

            self.binary_incidence_matrix[path] = self._get_binary_incidence_vector(file_content)

            file_.close()

    def _get_binary_incidence_vector(self, string):
        """Method to build a binary incidence vector based on the Model vocabulary list.
           1 - vocabulary word is in the string
           0 - vocabulary word isn't in the string

           @param string: :str:

           @return binary incidence :list:
        """
        binary_incidence_vector = []

        for word in self.vocabulary:
            binary_incidence_vector.append(1 if word in string else 0)

        return binary_incidence_vector

    ##################
    # PUBLIC METHODS #
    ##################

    def search(self, search_terms):
        """Method which processes an AND search of terms in the documents.
            @param search_terms: terms which will be searched in the documents.

            @return :list: of documents which has such terms.
        """
        search_terms_incidence_vector = self._get_binary_incidence_vector(search_terms)

        documents = []

        if not any(search_terms_incidence_vector):
            return documents

        for document_path, document_incidence_vector in self.binary_incidence_matrix.items():
            if (1, 0) not in zip(search_terms_incidence_vector, document_incidence_vector):
                documents.append(document_path)

        return documents
