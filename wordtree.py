from os.path import exists
from timeit import default_timer as timer
from pybktree import BKTree
import numpy
import json

# Encode BkTree to JSON
class BkTreeEncoder(json.JSONEncoder):

    def default(self, o: BKTree):
        if isinstance(o, int):
            return o

        if isinstance(o, BKTree):
            tupl = o.tree
            return tupl

        return super(BkTreeEncoder, self).default(o)

# Decode BKTree from JSON
class BkTreeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, obj):
        if isinstance(obj, dict):
            return { int(k): (v[0], self.object_hook(v[1])) for k,v in obj.items() }

        
        return obj

def _levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1), dtype='int32')

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
    return distances[len(token1)][len(token2)].item() # minimum edit distance + 1

word_tree: BKTree = None

# Read BKTree from file (FAST)
if exists("bktree.json"):
    with open("bktree.json", 'r') as f:
        json_str = f.read()
        word_tree = BKTree(_levenshteinDistanceDP)
        word_tree.tree = tuple(BkTreeDecoder().decode(json_str))
else:
    # Load dictionary words from file
    _dictionary_words = []
    with open('dictionary.txt', 'r') as dict_file:
        for line in dict_file.readlines():
            _dictionary_words.append(line.strip())

    # Create BKTree (VERY SLOW)
    word_tree = BKTree(_levenshteinDistanceDP, _dictionary_words)
    # Store BKTree to json for quick load
    json_str = json.dumps(word_tree, cls=BkTreeEncoder)
    with open("bktree.json", 'w') as f:
        f.write(json_str)
