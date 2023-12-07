from django.shortcuts import render
from .util import auto_correct, get_mismatch_dict
from .forms import TextCheckForm
import time

def readDict(first_letter):
    # with open('dictionaries/br-utf8.txt', 'r') as f:
    with open(f"dictionaries/words_by_first_letter/words_letter_{first_letter}.txt", "r") as f:
        word_dict = f.read().splitlines()
    return word_dict


def index(request):
    mismatch_dict = get_mismatch_dict()
    gap_weight = 5

    closest_word = ''
    input_word = ''

    if request.method == 'POST':
        form = TextCheckForm(request.POST)
        if request.POST.get('limpar', None):
            form = TextCheckForm()
            form.fields["word"].initial = ''
        if form.is_valid():
            input_word = form.cleaned_data['word'].lower()
            tokens = {}
            print("starting tokens")
            start_time = time.time()
            for token in input_word.split():
                word_dict = readDict(token[0])
                tokens[token] = auto_correct(token, word_dict, gap_weight, mismatch_dict)
            print(tokens)
            print(time.time() - start_time)
            #closest_word = auto_correct(input_word, word_dict, gap_weight, mismatch_dict)
            closest_word = ""
            return render(request, 'api/index.html', {'form': form, 'input_word': input_word, 'closest_word': closest_word})
    else:
        form = TextCheckForm(initial='')

    return render(request, 'api/index.html', {'form': form, 'input_word': input_word, 'closest_word': closest_word})
