from porter_stemmer import PorterStemmer

stemmer = PorterStemmer()

print stemmer.stem_word("adoption")
print stemmer.stem_word("controll")
print stemmer.stem_word("roll")
print stemmer.stem_word("agreed")
