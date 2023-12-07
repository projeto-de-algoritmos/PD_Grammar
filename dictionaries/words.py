with open("br-utf8.txt", "r") as dictionary:
    words = dictionary.readlines()
    for i in range(1, max([len(word.replace("\n", "")) for word in words]) + 1):
        file = open(f"words_len_{i}.txt", "a")
        for word in words:
            if len(word.replace("\n", "")) == i:
                file.write(word)