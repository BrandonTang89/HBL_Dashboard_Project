swear_words_file = "static/swear_words.txt"
with open(swear_words_file) as f:
    for line in f:
        print (line.strip())