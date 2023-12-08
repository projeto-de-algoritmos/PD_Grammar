from django.shortcuts import render
from .util import Trie
from .forms import TextCheckForm
import time
import datetime


def readDict():
    trie = Trie()

    with open("./word_dict.txt", 'r') as f:
        for w in f.read().split():
            trie.insert(w.lower())

    return trie


word_dict = None


def index(request):
    # Se ainda não tiver instanciado o dicionário, instancia
    global word_dict
    if word_dict is None:
        word_dict = readDict()

    closest_word = ''
    input_word = ''

    if request.method == 'POST':
        form = TextCheckForm(request.POST)
        if request.POST.get('limpar', None):
            form = TextCheckForm()
            form.fields["word"].initial = ''
        if form.is_valid():
            input_word = form.cleaned_data['word'].lower().split()
            gap_cost = form.cleaned_data['gap_cost']
            max_diff = form.cleaned_data['max_diff']

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
            return render(request, 'api/index.html', {'form': form, 'input_word': input_word, 'closest_word': formatted_output, 'time_passed': time_passed, 'visited_nodes': total_visited_nodes})
    else:
        form = TextCheckForm()
        
    return render(request, 'api/index.html', {'form': form, 'input_word': input_word, 'closest_word': closest_word})
