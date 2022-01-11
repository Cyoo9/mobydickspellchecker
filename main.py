import re
# f = open("mobydick.txt", 'r')
# data = f.readlines()
# print(data)

f2 = open("tokens.txt", 'r')
words = f2.readlines()
longest_word = ""
frequencies = {}

for word in words:
    if re.match('[a-zA-Z]', word):
        if(len(word) > len(longest_word)):
            longest_word = word
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

print("longest word: " + longest_word)

print("top 10 most frequent words: ")
sorted_words = sorted(frequencies)
for x in range(10):
    print(sorted_words[len(sorted_words) - 1 - x])

print("top 10 least frequent words: ")
for x in range(10):
    print(sorted_words[x])