from django.shortcuts import render
from core.decorators import *
from core.models import Word, Group, Sentence

@exception_wrapper(ajax_error)
@auth_required
def search(request):
    if request.method == 'POST':
        term = str(request.POST.get('search-term', '').strip())
        translations = Word.objects.filter(user=request.user, translation__contains=term)
        words = Word.objects.filter(user=request.user, signature__contains=term)
        groups = Group.objects.filter(user=request.user, name__contains=term)
        sentences = Sentence.objects.filter(user=request.user, body__contains=term)
    else:
        term = ''
    return render(request, 'page/search.html', locals())
