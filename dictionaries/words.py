# with open("br-utf8.txt", "r") as dictionary:
#     words = dictionary.readlines()
#     for i in range(1, max([len(word.replace("\n", "")) for word in words]) + 1):
#         file = open(f"words_len_{i}.txt", "a")
#         for word in words:
#             if len(word.replace("\n", "")) == i:
#                 file.write(word)

with open("br-sem-acentos.txt", "r") as dictionary:
    words = dictionary.readlines()
    for word in words:
        word = word.lower()
        first_letter = word[0]
        file = open(f"words_by_first_letter/words_letter_{first_letter}.txt", "a")
        file.write(word)