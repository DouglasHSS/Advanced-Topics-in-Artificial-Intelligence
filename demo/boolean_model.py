from boolean_model import BooleanModelInformationRetrieval

boolean_model = BooleanModelInformationRetrieval(["text.txt", "text2.txt", "text3.txt"])

print "monkey", boolean_model.search("monkey")
print "tiger", boolean_model.search("tiger")
print "running jungle", boolean_model.search("running jungle")
