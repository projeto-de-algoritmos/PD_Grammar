def levenshtein_distance(str1, str2, gap, mismatchs_dict):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1

    str1 = str1.lower()
    str2 = str2.lower()

    # Inicialização da matriz
    matrix = [[0 for _ in range(len_str2)] for _ in range(len_str1)]

    # Preenchimento da matriz com valores iniciais dos gaps
    for i in range(len_str1):
        matrix[i][0] = i * gap

    # Gaps na segunda string (dicionario) tem peso infinito
    for j in range(1, len_str2):
        matrix[0][j] = float('inf')

    # Cálculo da distância de edição
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            print(str1, str2)
            matrix[i][j] = min(
                matrix[i - 1][j - 1] + mismatchs_dict.get((str1[i - 1], str2[j - 1])),  # Mismatch
                matrix[i][j - 1] + gap,                # Gap em str1
                float('inf')                           # Gap em str2
            )

    return matrix[len_str1 - 1][len_str2 - 1]


def auto_correct(word, word_list, gap, mismatchs_dict):
    min_distance = float('inf')
    closest_word = ''

    for candidate in word_list:
        distance = levenshtein_distance(word, candidate, gap, mismatchs_dict)
        if distance < min_distance:
            min_distance = distance
            closest_word = candidate

    return closest_word


def get_mismatch_dict():
    # Criação do dicionário de pesos de mismatch
    keyboard = [
        ['q', 'w', 'e', 'é', 'ê','r', 't', 'y', 'u', 'ú', 'i', 'í', 'o', 'ó', 'ô','õ', 'p'],
        ['a', 'ã', 'á', 'à', 'â', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    ]

    key_positions = {key: (i, j) for i, row in enumerate(keyboard) for j, key in enumerate(row)}

    mismatchs_dict = {(key1, key2): abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) for key1, pos1 in key_positions.items() for key2, pos2 in key_positions.items()}

    return mismatchs_dict
