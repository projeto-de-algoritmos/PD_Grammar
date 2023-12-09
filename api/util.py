class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.mismatch_dict = self.__get_mismatch_dict()
        self.word_count = 0

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.word = word
        self.word_count += 1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.word == word


    def __get_mismatch_dict(self):
        # Criação do dicionário de pesos de mismatch
        keyboard = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]

        key_positions = {key: (i, j) for i, row in enumerate(keyboard) for j, key in enumerate(row)}

        mismatchs_dict = {(key1, key2): abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) for key1, pos1 in key_positions.items() for key2, pos2 in key_positions.items()}

        return mismatchs_dict

    def auto_correct(self, word, maxCost, gapCost):
        # Preenchimento da primeira linha da matriz com o
        currentRow = [i * gapCost for i in range(len(word) + 1)]

        results = []

        global visited_nodes
        visited_nodes = 0

        # Pesquisa cada ramo da trie recursivamente
        for char in self.root.children:
            self.levenshtein_distance(self.root.children[char], char, word, currentRow, results, maxCost, gapCost)

        return (min(results, key=lambda x: x[1]), visited_nodes) if results else ([], visited_nodes)

    def levenshtein_distance(self, node, char, word, previousRow, results, maxCost, gapCost):
        global visited_nodes
        visited_nodes += 1
        cols = len(word) + 1

        # O custo de gaps nas palavras do dicionario é infinito, pois elas já estão corretas
        currentRow = [float("inf")]

        # Cada linha é um novo caractere da trie e cada coluna um caractere da palavra a ser corrigida
        for col in range(1, cols):
            gap = previousRow[col] + gapCost
            mismatch = previousRow[ col - 1 ] + self.mismatch_dict.get((word[col - 1], char))

            currentRow.append(min(gap, mismatch))

        # Caso haja uma palavra já formada com custo menor do que o parâmetro maxCost, adiciona ela ao resultado
        if currentRow[-1] <= maxCost and node.word is not None:
            results.append((node.word, currentRow[-1]))

        # Caso haja alguma célula com custo menor do que o parâmetro maxCost, chama a função recursivamente para aquele ramo da trie
        if min(currentRow) <= maxCost:
            for char in node.children:
                self.levenshtein_distance(node.children[char], char, word, currentRow, results, maxCost, gapCost)
