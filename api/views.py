from django.shortcuts import render
from .util import auto_correct, get_mismatch_dict
from .forms import TextCheckForm


def readDict():
    with open('word_dict.txt', 'r') as f:
        word_dict = f.read().splitlines()

    return word_dict


def index(request):
    word_dict = readDict()
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
            input_word = form.cleaned_data['word']
            closest_word = auto_correct(input_word, word_dict, gap_weight, mismatch_dict)

            return render(request, 'api/index.html', {'form': form, 'input_word': input_word, 'closest_word': closest_word})
    else:
        form = TextCheckForm(initial='')

    return render(request, 'api/index.html', {'form': form, 'input_word': input_word, 'closest_word': closest_word})
