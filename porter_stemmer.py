# -*- coding: utf-8 -*-


class PorterStemmer(object):

    # ###################
    # # PRIVATE METHODS #
    # ###################

    def _step_1a(self, word):
        """Method which executes step 1a of Porter stemming algorithm.
            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        sufixes = [("sses", "ss"),
                   ("ies", "i"),
                   ("ss", "ss"),
                   ("s", "")]

        for sufix, replacement in sufixes:
            if sufix in word:
                return word.replace(sufix, replacement)
        return word

    # ##################
    # # PUBLIC METHODS #
    # ##################

    def stem_word(self, word):
        """Method which executes the stemming process in a word.
            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        word = word.lower()  # enforces lowercase

        stem = self._step_1a(word)

        return stem
