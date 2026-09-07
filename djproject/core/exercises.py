from django.shortcuts import render_to_response
from datetime import datetime
import random
from core.models import Word, Group, Record, Exercise
from core.decorators import *
from core.config import get_config_obj
from core.entities import get_paginator
import settings 
from django.core.mail import EmailMultiAlternatives

#*********************************************************
#******************** VIEWS
#*********************************************************
@exception_wrapper(ajax_upload_error)
@auth_required
def exercise(request, id):
    exercise = Exercise.objects.get(id=int(id))
    exercise_answer(exercise, request)       
    (all_words_len, success_words_len, remain_words) = get_exercise_remained_words(exercise, request.user);
    words_dict = {'all': all_words_len, 'success': success_words_len, 'failed': all_words_len - len(remain_words) - success_words_len} 
    if remain_words:
        next_word = remain_words[random.randint(0, len(remain_words) - 1)]
        return show_next_word(exercise, next_word, request.user, words_dict)
    else:
        exercise.finished = datetime.now()
        exercise.save()
        # get all failed words and send them via email
        failed_words = [record.word for record in Record.objects.filter(exercise=exercise, is_passed=False)]    
        mail_html_content = '%s%s%s' % ('<p style="font:18px Georgia,Serif">',''.join(['<b>%s</b>: %s<br/>' % (word.signature, word.translation) for word in failed_words]),'</p>')
        msg = EmailMultiAlternatives('[ETRAINER] Errors in exercise %s' % exercise.title, '', settings.ADMIN_EMAIL, ['goloniko@gmail.com'])
        msg.attach_alternative(mail_html_content, "text/html")
        msg.send(fail_silently=True)
        #send_mail('[ETRAINER] Errors in exercise %s' % exercise.title, mail_text, settings.ADMIN_EMAIL, ['goloniko@gmail.com'])
        return render_to_response('exercise/end.html', {'words': words_dict, 'exercise': exercise})            

@exception_wrapper(ajax_upload_error)
@auth_required
def get_records(request, id):
    exercise = Exercise.objects.get(id=int(id))
    entities_per_page = get_config_obj(request).entities_per_page
    sort_by = request.GET.get('sort', '?')
    paged_entities = get_paginator(get_sorted_records(request.user, exercise, sort_by), request.GET.get('page', '1'), entities_per_page)
    return render_to_response('exercise/get_records.html', {'exercise': exercise, 'entities': paged_entities, 'sort_by': sort_by})


#*********************************************************
#******************** INNER FUNCTIONS
#*********************************************************
def get_exercise_remained_words(exercise, user):
    # get all exercise words
    all_exercise_words = exercise.group and exercise.group.word_set.all() or Word.objects.filter(user=user) 
    if exercise.from_date:
        all_exercise_words = all_exercise_words.filter(created__gte=exercise.from_date)
    if exercise.to_date:
        all_exercise_words = all_exercise_words.filter(created__lte=exercise.to_date)
    if exercise.speech_part:
        all_exercise_words = all_exercise_words.filter(speech_part=exercise.speech_part)
    if exercise.failed:
        all_exercise_words = all_exercise_words.filter(failed__gte=exercise.failed)
    all_exercise_words = all_exercise_words.filter(is_active=True)
    # get all passed words 
    all_passed_words = [record.word for record in Record.objects.filter(exercise=exercise)]    
    # get all success passed words 
    all_success_words = [record.word for record in Record.objects.filter(exercise=exercise, is_passed=True)]    
    # return anti-intersection of two lists
    return (len(all_exercise_words), len(all_success_words), [word for word in list(all_exercise_words) if word not in all_passed_words])
  
def exercise_answer(exercise, request):
    if exercise.exercise_type.id == 1:
        choose_translation_answer(exercise, request)
    elif exercise.exercise_type.id == 2:
        write_word_answer(exercise, request)
    elif exercise.exercise_type.id == 3:
        sentences_answer(exercise, request)

def choose_translation_answer(exercise, request):
    word_id = request.GET.get('w', None)
    is_passed = request.GET.get('p', None)
    if word_id and is_passed:
        word = Word.objects.get(id=int(word_id))
        new_record(word, exercise, int(is_passed))

def write_word_answer(exercise, request):
    signature = request.POST.get('test-sign', None)
    real = request.POST.get('real', None)
    word_id = request.POST.get('id', None)
    if real and word_id:
        word = Word.objects.get(id=int(word_id))
        is_passed = bool(real==signature)
        new_record(word, exercise, is_passed)

def sentences_answer(exercise, request):
    word_id = request.GET.get('id', None)
    if word_id:
        word = Word.objects.get(id=int(word_id))
        new_record(word, exercise, True)

def new_record(word, exercise, is_passed):
    records = Record.objects.filter(word=word, exercise=exercise, is_passed=is_passed)
    if len(records) == 0:
        if is_passed:
            word.success += 1
        else:
            word.failed += 1
        word.save()
        Record.objects.create(word=word, exercise=exercise, is_passed=is_passed)

def show_next_word(exercise, next_word, user, words_dict):
    if exercise.exercise_type.id == 1:
        return show_choose_translation(exercise, next_word, user, words_dict)
    elif exercise.exercise_type.id == 2:
        return show_write_word(exercise, next_word, words_dict)
    elif exercise.exercise_type.id == 3:
        return show_sentences(exercise, next_word, words_dict)
    
def show_choose_translation(exercise, next_word, user, words_dict):
    except_list = [next_word] + list(next_word.synonyms.all()) 
    variants = [w for w in list(Word.objects.filter(user=user, speech_part=next_word.speech_part).order_by('?')) if w not in except_list][:5]
    slice_num = random.randint(0, 5)
    variants = [variants[:slice_num], variants[slice_num:]]
    return render_to_response('exercise/choose_translation.html', {'next_word': next_word, 'variants': variants, 'exercise': exercise, 'words': words_dict})    

def show_write_word(exercise, next_word, words_dict):
    return render_to_response('exercise/write_word.html', {'word': next_word, 'exercise': exercise, 'words': words_dict})

def show_sentences(exercise, next_word, words_dict):
    return render_to_response('exercise/sentences.html', {'w': [next_word], 'exercise': exercise, 'words': words_dict})

def get_sorted_records(user, exercise, sort_by):
    if sort_by not in ['word', 'timestamp', 'is_passed']:
        sort_by = 'timestamp'
    return Record.objects.filter(exercise=exercise).order_by(sort_by)
