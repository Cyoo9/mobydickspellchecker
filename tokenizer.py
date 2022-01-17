from nltk.tokenize import word_tokenize
import re
from collections import deque

# Load contractions
# Contractions were taken from https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
contractions: dict[str, tuple[str]] = {}
with open("contractions.txt", 'r') as c_f:
    lines = c_f.readlines()
    for line in lines:
        line = line.strip()
        split = line.split(" ")
        contractions[split[0]] = tuple(split[1:])


# Split string into a list of words
# - Removes punctuation
# - Expands contractions
# - Lowercase all tokens
def word_tokenize_txt(data: str) -> list[str]:
    # Perform first-pass tokenization using NLTK
    tokens = word_tokenize(data)
    alpha_regex=re.compile("[a-zA-Z]+")
    # Perform filtering
    filtered = deque()
    skip_word = False
    # Loop through the text backwords
    for i in reversed(range(len(tokens))):
        if skip_word:
            skip_word = False
            continue

        curr_word = tokens[i]
        # Filter out punctuations, numbers, and possessions from the list.
        if not alpha_regex.search(curr_word) or curr_word == "'s":
            continue
        
        # Check if the current word is the ending of a contraction
        if (curr_word == "n't" or curr_word.startswith("'")) and i > 0:
            # Check if the previous word (e.g "are") + current word (e.g "n't") is a contracted word (e.g. aren't)
            prev_word = tokens[i - 1]
            combined_word = prev_word + curr_word
            lower_case = combined_word.lower()

            if lower_case in contractions:
                # If the word is a contraction, expand it out using the contractions dictionary
                for word in reversed(contractions[lower_case]):
                    filtered.appendleft(word)

                # Skip the previous word since it's the beginning of the contraction
                skip_word = True
                continue
            
        # Push word to the beginning
        filtered.appendleft(curr_word.lower())
    
    return list(filtered)