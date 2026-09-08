# coding=utf-8
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime
import core.forms
from core.models import Word, Group, Sentence, Record, Exercise, Config
import core.models as model
from core.decorators import *
from core.config import get_config_page, get_config_obj

#*********************************************************
#******************** VIEWS
#*********************************************************
@exception_wrapper(ajax_error)
@auth_required
def get_all(request, entity):
    Entity = get_class(entity)
    entities_per_page = get_config_obj(request).entities_per_page
    sort_by = request.GET.get('sort', '?')
    paged_entities = get_paginator(get_sorted_entities(request.user, Entity, sort_by), request.GET.get('page', '1'), entities_per_page)
    return render(request, 'entity/get_all.html', {'Entity': Entity, 'entities': paged_entities, 'sort_by': sort_by})

@exception_wrapper(ajax_error)
@auth_required
def get(request, entity, id):
    Entity = get_class(entity)
    obj = Entity.objects.get(id=int(id))
    return render(request, 'entity/get_%s.html' % entity, {entity: obj, 'Entity': Entity})

@exception_wrapper(ajax_error)
@auth_required
def add(request, entity):
    return add_update(request, entity)

@exception_wrapper(ajax_error)
@auth_required
def update(request, entity, id):
    return add_update(request, entity, id)

@exception_wrapper(ajax_error)
@auth_required
def remove(request, entity, id):
    classObj = get_class(entity)
    obj = classObj.objects.get(id=int(id), user=request.user)
    obj.delete()
    return get_all(request, entity)

@exception_wrapper(ajax_error)
@auth_required
def remove_some(request, entity):
    classObj = get_class(entity)
    if len(request.POST) != 0:
        for id, val in request.POST.items():
            obj = classObj.objects.get(id=int(id), user=request.user)
            obj.delete()
    return get_all(request, entity)

@exception_wrapper(ajax_error)
@auth_required
def set_words_active(request):
    return set_active(request, True)

@exception_wrapper(ajax_error)
@auth_required
def set_words_inactive(request):
    return set_active(request, False)

@exception_wrapper(ajax_error)
@auth_required
def page(request, name):
    if name == 'index':
        return render(request, 'page/%s.html' % name)
    elif name in ['word', 'group', 'sentence', 'exercise']:
        return get_all(request, name)
    elif name == 'config':
        return get_config_page(request)

@exception_wrapper(ajax_error)
@auth_required
def change_word(request, id, what):
    """
    what = 'sentences' || 'groups' || 'synonyms'
    """
    word = Word.objects.get(id=int(id), user=request.user)
    if what in ['synonyms', 'groups', 'sentences']:
        if request.method == 'GET':
            return render(request, 'entity/change_word_%s.html' % (what,), {'word': word})
        else:
            getattr(word, what).clear()
            entities = request.POST.getlist(what)
            if entities:
                for e in entities:
                    getattr(word, what).add(get_change_class(what).objects.get(id=int(e)))
                word.save()
            return get(request, 'word', id)
    else:
        raise ValueError('Incorrect request.')

@exception_wrapper(ajax_error)
@auth_required
def change_words(request, id, who):
    """
    who = 'sentence' || 'group'
    """
    entity = get_class(who).objects.get(id=int(id), user=request.user)
    if request.method == 'GET':
        return render(request, 'entity/change_%s.html' % who, {'entity': entity})
    else:
        entity.word_set.clear()
        words = request.POST.getlist('words')
        if words:
            for w in words:
                entity.word_set.add(Word.objects.get(id=int(w)))
            entity.save()
        return get(request, who, id)

@exception_wrapper(ajax_error)
@auth_required
def change_get_entities(request, what):
    term = str(request.POST.get('term', '')).strip()
    word_id = request.POST.get('word_id', '')
    if word_id == '':
        raise ValueError('Param "word_id" cannot be null.')
    if term == '':
        entities = []
    elif what == 'words':
        entities = Word.objects.filter(user=request.user, signature__startswith=term).exclude(id=int(word_id))
    elif what == 'groups':
        entities = Group.objects.filter(user=request.user, name__contains=term)
    else:
        entities = Sentence.objects.filter(user=request.user, body__contains=term)
    return render(request, 'entity/change_get_entities.html', {'entities': entities})

#*********************************************************
#******************** INNER FUNCTIONS
#*********************************************************
def add_update(request, entity, id=None):
    '''
    Common function for add and update actions. 
    '''
    classObj = get_class(entity)
    formCls = get_form(entity) 

    obj = id and classObj.objects.get(id=int(id), user=request.user) or None
        
    if request.method == 'POST': 
        form = formCls(request.user, request.POST, instance=obj)
        if form.is_valid(): 
            new_entity = form.save(commit=False)
            form.cleaned_data['user'] = request.user 
            new_entity.user = request.user
            if not id:
                new_entity.created = datetime.now()
            new_entity.save()
            return render(request, 'entity/get_%s.html' % entity, {entity: new_entity, 'Entity': classObj})
    else:
        form = formCls(request.user, instance=obj) 

    context = {'Entity': classObj, 'form': form}
    addition_context = id and \
        {'entity': obj, 'btn_link': obj.ajax_update(), 'btn_value': u'редактировать'} or \
        {'btn_link': classObj.ajax_add(), 'btn_value': u'создать'}
    context.update(addition_context)
    
    return render(request, 'entity/add_or_update.html', context)

def get_class(entity):
    return getattr(model, str(entity).capitalize())

def get_change_class(entities):
    if entities == 'synonyms':
        return getattr(model, 'Word')
    elif entities == 'groups':
        return getattr(model, 'Group')
    else:
        return getattr(model, 'Sentence')

def get_form(entity):
    return getattr(core.forms, '%sForm' % str(entity).capitalize())

def get_sorted_entities(user, Entity, sort_by):
    if not sort_by in ['name', 'success', 'failed', 'created', 'finished', 'word_set', 'speech_part__name', 'exercise_type', 'is_active']:
        sort_by = '-created'
    if sort_by == 'name':
        sort_by = (Entity.__name__ == 'Word' and 'signature') or \
                  (Entity.__name__ == 'Sentence' and 'body') or \
                  (Entity.__name__ == 'Group' and 'name') or \
                  (Entity.__name__ == 'Exercise' and 'title')
    if sort_by in ['success', 'failed']:
        sort_by = "-%s" % sort_by
    if sort_by == 'word_set':
        return Entity.objects.annotate(word_count = Count('word')).filter(user=user).order_by('-word_count')
    qs = Entity.objects.filter(user=user).order_by(sort_by)
    if Entity.__name__ == 'Word':
        qs = qs.select_related('speech_part')
    elif Entity.__name__ == 'Exercise':
        qs = qs.select_related('exercise_type')
    return qs

def get_paginator(entities, page, per_page): 
    try:
        page = int(page)
    except ValueError:
        page = 1

    paginator = Paginator(entities, per_page)

    # If page request (9999) is out of range, deliver last page of results.
    try:
        p_entities = paginator.page(page)
    except (EmptyPage, InvalidPage):
        p_entities = paginator.page(paginator.num_pages)
    
    return p_entities   

def set_active(request, is_active):
    if len(request.POST) != 0:
        for id, val in request.POST.items():
            obj = Word.objects.get(id=int(id), user=request.user)
            obj.is_active = is_active
            obj.save()
    return get_all(request, 'word')
