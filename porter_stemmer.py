# -*- coding: utf-8 -*-


class PorterStemmer(object):

    VOWELS = "aeiou"

    # ###################
    # # PRIVATE METHODS #
    # ###################
    def _has_vowels(self, word):
        """Method which checks whether a word has vowels or not.

            @param word: word :str: that is being stemmed.

            @return: :boolean:
        """
        for vowel in self.VOWELS:
            if vowel in word:
                return True
        return False

    def _is_vowel(self, word, char_index):
        """Method which identifies whether a character is a vowel or not.

            @param word: word :str: that is being stemmed.
            @param char_index: letter position :int: in the word.

            @return: :boolean:
        """
        if word[char_index] in self.VOWELS:
            return True

        elif word[char_index] == "y" and char_index > 0:
            return not self._is_vowel(word, char_index - 1)

        else:
            return False

    def _measures_word(self, word):
        """Method which count the number of VC in a word.
            A C represents a sequence of consonants(c), while a V denotes a sequence of vowels(v).

            @param word: word :str: that is being stemmed.

            @return: quantity of "VC" in inputted word.
        """
        vc_chain = ""
        for char_index, _ in enumerate(word):
            if self._is_vowel(word, char_index):
                vc_chain += "v"
            else:
                vc_chain += "c"

        return vc_chain.count("vc")

    def _step_1a(self, word):
        """Method which executes step 1a of the Porter stemming algorithm.

            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        sufixes = [("sses", "ss"),
                   ("ies", "i"),
                   ("ss", "ss"),
                   ("s", "")]

        for sufix, replacement in sufixes:
            if word.endswith(sufix):
                return word.replace(sufix, replacement)
        return word

    def _step_1b(self, word):
        """Method which executes step 1b of the Porter stemming algorithm.

            @param word: word :str: that is being stemmed.

            @return: word stem :str:
        """

        def _ends_with_double_consonants(stem):
            """Function which checks if a stem ends with double consonants.

                @param stem: stem :str: to be checked.

                @return: :boolean:
             """
            return (len(stem) > 1 and
                    not self._is_vowel(stem, -1)
                    and stem[-1] == stem[-2])

        def _ends_with_cvc(stem):
            """Function which checks if a stem ends with a consonant, a vowel and a consonant
                respectively.

                @param stem: stem :str: to be checked.

                @return: :boolean:
             """
            return (len(stem) > 2 and
                    not self._is_vowel(stem, -3) and
                    self._is_vowel(stem, -2) and
                    not self._is_vowel(stem, -1))

        if word.endswith("eed"):
            stem = word.replace("eed", "ee")
            return stem if self._measures_word(stem) > 0 else word

        apply_complementary_rules = False
        for sufix in ["ed", "ing"]:
            if word.endswith(sufix):
                stem = word.replace(sufix, "")
                if self._has_vowels(stem):
                    apply_complementary_rules = True

        if not apply_complementary_rules:
            return word

        for sufix in ["at", "bl", "iz"]:
            if stem.endswith(sufix):
                return stem + "e"

        if stem[-1] not in "lsz" and _ends_with_double_consonants(stem):
            return stem[:-1]

        if self._measures_word(stem) == 1 and _ends_with_cvc(stem) and stem[-3] not in "wxy":
            return stem + "e"

        return stem

    def _step_1c(self, word):
        """Method which executes step 1c of the Porter stemming algorithm.

            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        if word.endswith("y") and self._has_vowels(word):
            return word.replace("y", "i")
        return word

    def _step_2(self, word):
        """Method which executes step 2 of the Porter stemming algorithm.

            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        sufixes = [("ational", "ate"), ("tional", "tion"), ("enci", "ence"),
                   ("anci", "ance"), ("izer", "ize"), ("abli", "able"),
                   ("alli", "al"), ("eli", "e"), ("entli", "ent"),
                   ("ousli", "ous"), ("ization", "ize"), ("ation", "ate"),
                   ("ator", "ate"), ("alism", "al"), ("iveness", "ive"),
                   ("fulness", "ful"), ("ousness", "ous"), ("aliti", "al"),
                   ("iviti", "ive"), ("biliti", "ble")]

        for sufix, replacement in sufixes:
            if word.endswith(sufix):
                stem = word.replace(sufix, "")
                if self._measures_word(stem) > 0:
                    return stem + replacement
        return word

    def _step_3(self, word):
        """Method which executes step 3 of the Porter stemming algorithm.

            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        sufixes = [("icate", "ic"),
                   ("ative", ""),
                   ("alize", "al"),
                   ("iciti", "ic"),
                   ("ical", "ic"),
                   ("ful", ""),
                   ("ness", "")]

        for sufix, replacement in sufixes:
            if word.endswith(sufix):
                stem = word.replace(sufix, "")
                if self._measures_word(stem) > 0:
                    return stem + replacement
        return word

    def _step_4(self, word):
        """Method which executes step 4 of the Porter stemming algorithm.

            @param word: word :str: that should be stemmed.

            @return: word stem :str:
        """
        sufixes = [("al", ""), ("ance", ""), ("ence", ""), ("er", ""),
                   ("ic", ""), ("able", ""), ("ible", ""), ("ant", ""),
                   ("ement", ""), ("ment", ""), ("ent", "")]

        for sufix, replacement in sufixes:
            if word.endswith(sufix):
                stem = word.replace(sufix, "")
                if self._measures_word(stem) > 1:
                    return stem + replacement

        if word.endswith("ion"):
            stem = word.replace(sufix, "")
            if self._measures_word(stem) > 1 and stem[-1] in "st":
                return stem

        sufixes = [("ou", ""), ("ism", ""), ("ate", ""), ("iti", ""),
                   ("ous", ""), ("ive", ""), ("ize", "")]

        for sufix, replacement in sufixes:
            if word.endswith(sufix):
                stem = word.replace(sufix, "")
                if self._measures_word(stem) > 1:
                    return stem + replacement

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
        stem = self._step_1b(stem)
        stem = self._step_1c(stem)
        stem = self._step_2(stem)
        stem = self._step_3(stem)
        stem = self._step_4(stem)

        return stem
