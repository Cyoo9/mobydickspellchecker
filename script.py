import numpy
import re
from timeit import default_timer as timer
from tokenizer import word_tokenize_txt
from wordtree import word_tree

def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1] #i, j-1
                b = distances[t1 - 1][t2] #i-1, j
                c = distances[t1 - 1][t2 - 1] #i-1, j-1
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    # printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)] # minimum edit distance + 1

## Print the edit distances for DEBUG purposes
# def printDistances(distances, token1Length, token2Length):
#     for t1 in range(token1Length + 1):
#         for t2 in range(token2Length + 1):
#             print(int(distances[t1][t2]), end=" ")
#         print()

# Load the dictionary file into a set of words
dictionary_words: set[str]=set()
with open('dictionary.txt', 'r') as dict_file:
    for line in dict_file.readlines():
        dictionary_words.add(line.strip())

# def calcDictDistance(word, numWords):
#     word_distances: list[tuple[str, int]] = []

#     # Go through all the words in the dictionary
#     for dict_word in dictionary_words:
#         word_dist = levenshteinDistanceDP(word, dict_word)
#         if word_dist >= 10:
#             word_dist = 9

#         # Add the word distances to the list
#         word_distances.append((dict_word, word_dist))
    
#     # Sort the list
#     word_distances.sort(key=lambda tup: tup[1])

#     return [ word_distances[i][0] for i in range(numWords) ]

corrected_words = { }
def get_correct_words(word: str, numWords: int) -> list[str]:
    results = None
    # Check if same word has already been corrected
    if word in corrected_words:
        results = corrected_words[word]
    else:
        # Use the word tree to find all words w/ a min edit distance of <= 4 compared to the word
        results = sorted(word_tree.find(word, 4))
        corrected_words[word] = results

    return [ results[i][1] for i in range(min(len(results), numWords)) ]

tokens = []

with open("./mobydick.txt", 'r') as f:
    tokens = word_tokenize_txt(f.read())

for word in tokens:
    if word not in dictionary_words:
        suggestions = get_correct_words(word, 3)
        if(len(suggestions) > 0):
            print(word + ": " + str(suggestions))