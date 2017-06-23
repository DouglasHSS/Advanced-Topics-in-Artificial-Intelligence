# -*- coding: utf-8 -*-
import nltk

from math import log
from string import punctuation

from utils import initialize_nltk_tokenizer, initialize_nltk_stopwords


class Sumarizador(object):

    def __init__(self, caminho_documento=None):
        if caminho_documento is None:
            raise "Caminho do do texto deve ser informado."

        documento = open(caminho_documento, "r")
        self.texto = "".join(documento.readlines()).decode("utf-8")
        self.tf_palavras = {}
        self.idf_palavras = {}
        self.sentencas_pontuadas = []

        initialize_nltk_tokenizer()
        initialize_nltk_stopwords()

        self._separar_sentencas()
        self._separar_palavras()

    ###################
    # PRIVATE METHODS #
    ###################

    def _separar_sentencas(self):
        self.sentencas = nltk.tokenize.sent_tokenize(self.texto)
        self.total_sentencas = len(self.sentencas)

    def _separar_palavras(self):
        palavras = [palavra for palavra in nltk.tokenize.word_tokenize(self.texto)
                    if palavra not in punctuation]
        self.total_palavras = len(palavras)
        self.palavras = set(palavras)

    def _calcular_tfs(self):
        """Método que cálcula o TF de uma palavra
           Calculo do TF de uma palavra: qtd da palavra no texto/total de palavras no texto.
        """
        for palavra in self.palavras:
            tf = float(self.texto.count(palavra)) / float(self.total_palavras)
            self.tf_palavras[palavra] = tf

    def _calcular_idfs(self):
        """Método que cálcula o IDF de uma palavra
        """
        for palavra in self.palavras:
            ocorrencias = sum([1 for sentenca in self.sentencas if palavra in sentenca])
            if ocorrencias > 0:
                idf = log(float(self.total_sentencas+1) / float(ocorrencias))
                self.idf_palavras[palavra] = idf

    def _pontuar_sentencas(self):
        for sentenca in self.sentencas:
            pontuacao = sum([self.tf_palavras.get(palavra, 0) *
                             self.idf_palavras.get(palavra, 0)
                             for palavra in nltk.tokenize.word_tokenize(sentenca)])
            self.sentencas_pontuadas.append((sentenca, pontuacao))

        self.sentencas_pontuadas = sorted(self.sentencas_pontuadas,
                                          key=lambda x: x[1])[::-1]

    ###################
    # PUBLIC METHODS #
    ###################

    def sumarizar_texto(self):
        self._calcular_tfs()
        self._calcular_idfs()

        self._pontuar_sentencas()

        return " ".join(sentenca for sentenca, _ in self.sentencas_pontuadas[:3])
