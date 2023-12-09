from django.shortcuts import render
from .util import Trie
from .forms import TextCheckForm, AddWordForm
import time
import datetime


def readDict():
    trie = Trie()

    with open("./word_dict.txt", 'r') as f:
        for w in f.read().split():
            trie.insert(w.lower())

    return trie


def addWord(new_word):
    with open("./word_dict.txt", 'a') as f:
        f.write(new_word  + "\n")

    global was_dict_modified
    was_dict_modified = 1


word_dict = None
was_dict_modified = 0


def index(request):
    # Se ainda não tiver instanciado o dicionário ou
    # ele tiver sido modificado, cria uma nova instância

    global word_dict, was_dict_modified

    if word_dict is None or was_dict_modified:
        word_dict = readDict()
        was_dict_modified = 0

    closest_word = ''
    input_word = ''

    if request.method == 'POST':
        checkerForm = TextCheckForm(request.POST)
        adderForm = AddWordForm(request.POST)

        if request.POST.get('limpar', None):
            checkerForm = TextCheckForm()
            checkerForm.fields["word"].initial = ''

        if checkerForm.is_valid():
            input_word = checkerForm.cleaned_data['word'].lower().split()
            gap_cost = checkerForm.cleaned_data['gap_cost']
            max_diff = checkerForm.cleaned_data['max_diff']

            tic = time.time()
            tokens = {}
            total_visited_nodes = 0
            for token in input_word:
                closest_word, visited_nodes = word_dict.auto_correct(token, max_diff, gap_cost)
                tokens[token] = closest_word[0] if closest_word else ""
                total_visited_nodes += visited_nodes
            tac = time.time()

            # Formatando a saída para exibição
            formatted_output = " ".join(list(tokens.values())) if list(tokens.values()) != list(tokens.keys()) else []

            # Formatando o tempo gasto em um formato legível
            time_passed = " minutos e ".join(str(datetime.timedelta(seconds=tac - tic))[2:-3].split(":")) + " segundos"

            return render(request, 'api/index.html', {'checkerForm': checkerForm, 'adderForm': adderForm, 'input_word': input_word, 'closest_word': formatted_output, 'time_passed': time_passed, 'visited_nodes': total_visited_nodes, 'word_count': word_dict.word_count})

        if adderForm.is_valid():
            print(adderForm.is_valid())
            new_word = adderForm.cleaned_data['new_word'].lower()
            # if new_word:
            addWord(new_word)

            checkerForm = TextCheckForm()
            adderForm = AddWordForm()

            return render(request, 'api/index.html', {'checkerForm': checkerForm, 'adderForm': adderForm, 'word_count': word_dict.word_count})

    else:
        checkerForm = TextCheckForm()
        adderForm = AddWordForm()

    return render(request, 'api/index.html', {'checkerForm': checkerForm, 'adderForm': adderForm, 'input_word': input_word, 'closest_word': closest_word, 'word_count': word_dict.word_count})
