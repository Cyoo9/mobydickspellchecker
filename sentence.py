from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

f = open("mobydick.txt", 'r')
data = f.readlines()

print(len(word_tokenize(str(data))))

print(len(sent_tokenize(str(data))))
