# coding=utf-8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
import csv, re
from datetime import datetime
from core.models import Word, SpeechPart, Group, Sentence, Config
from core.decorators import *
from core.forms import ExportForm

#*********************************************************
#******************** VIEWS
#*********************************************************
@exception_wrapper(ajax_upload_error)
@auth_required
def export(request, what):
	if request.method == 'GET':
		form = ExportForm(request.user)
		return render_to_response('page/export_%s.html' % what, {'form': form})
	else:
		response = HttpResponse(mimetype='text/csv')
		form = ExportForm(request.user, request.POST)
		if form.is_valid(): 
			words = Word.objects.filter(user=request.user)
			cleaned = form.cleaned_data
			if cleaned['from_date']:
				words = words.filter(created__gte=cleaned['from_date'])
			if cleaned['to_date']:
				words = words.filter(created__lte=cleaned['to_date'])
			if cleaned['groups']:
				words = words.filter(groups__in=cleaned['groups'])
			if cleaned['speechparts']:
				words = words.filter(speech_part__in=cleaned['speechparts'])
			words = words.distinct()
			response['Content-Disposition'] = ('attachment; filename=%s' % (what == 'csv' and 'words.csv' or 'sentences_%s.html' % cleaned['from_date'],))
			return what == 'csv' and get_csv_from_words(response, words) or get_html_from_words(response, words)
		else:
			response['Content-Disposition'] = 'attachment; filename=errors.log'			 	
			return get_export_errors(response, form.errors)

@exception_wrapper(ajax_upload_error)
@auth_required
def csv_import(request):
    if request.method == 'POST':
        file = request.FILES['userfile']
        words = get_words_from_csv(read_csv_file(file), request.user)
        return render_to_response('ajax_success.html', {'message':  u'Успешно! Всего слов загружено - %d.' % len(words)})
    else:
        raise Exception

@exception_wrapper(ajax_error)
@auth_required
def remove_all(request):
    Group.objects.filter(user=request.user).delete()
    Sentence.objects.filter(user=request.user).delete()
    Word.objects.filter(user=request.user).delete()
    return get_config_page(request)

@exception_wrapper(ajax_error)
@auth_required
def set_entities_per_page(request):
    config = Config.objects.get(user=request.user)
    new_val = int(request.GET.get('entities_per_page', None))
    config.entities_per_page = new_val
    config.save()
    return get_config_page(request)

#*********************************************************
#******************** INNER FUNCTIONS
#*********************************************************
def get_config_page(request):
    config = get_config_obj(request)
    return render_to_response('page/config.html', locals())

def get_config_obj(request):
    try:
        config = Config.objects.get(user=request.user)
    except Config.DoesNotExist, e:
        Config.objects.create(user=request.user)
    config = Config.objects.get(user=request.user)
    return config

def get_csv_from_words(response, words):
    '''
    Function gets all words of user 
    and write them to response variable in CSV format. 
    '''
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['signature', 'translation', 'speech part', 'transcription', 'synonyms', 'sentences', 'groups'])
    for word in words:
        writer.writerow([word.signature,
                         word.translation.encode('utf_8'), 
                         word.speech_part, 
                         word.transcription.encode('utf_8'),
                         (', '.join([synonym.signature for synonym in word.synonyms.all()])).encode('utf_8'),
                         (' | '.join([sentence.translation and '%s[%s]' % (sentence.body, sentence.translation) or sentence.body for sentence in word.sentences.all()])).encode('utf_8'),
                         (', '.join([group.name for group in word.groups.all()])).encode('utf_8')
                         ])
    return response

def get_html_from_words(response, words):
    '''
    Function gets all expressions of user 
    and write them to response variable in HTML format. 
    sentences_export.html
    '''
    sentences = Sentence.objects.filter(word__in=words)
    sentences = sentences.distinct()
    t = get_template('page/sentences_export.html')
    response.write(t.render(Context({'sentences': sentences, 'words': words})))
    return response

def get_export_errors(response, errors):
    writer = csv.writer(response, delimiter=';')
    for e in [v for k, v in errors.items()]:
        writer.writerow([e])
    return response

def read_csv_file(file):
    csv_data = str()
    for chunk in file.chunks():
        csv_data += chunk
    return csv_data.split('\r\n')

def get_words_from_csv(csv_data, user):
    '''
    Function reads CSV data and adds words to system. 
    '''
    if not csv_data: 
        raise ValueError('Неправильный формат данных: пустой файл.')
    reader = csv.reader(csv_data, delimiter=';')
    words = list()
    now = datetime.now()
    try:
        for i, row in enumerate(reader):
            if i == 0:
                # checking data: header 
                if ';'.join(row) != 'signature;translation;speech part;transcription;synonyms;sentences;groups':
                    raise ValueError('Неправильный формат данных: неверный заголовок CSV файла.')
            if i > 0:
                # checking data: number of words
                if len(row) == 7:
                    # checking data: signature and translation can't be empty
                    if not (row[0] and row[1]):
                        raise ValueError('Неправильный формат данных: отсутствует слово и/или перевод.', 'Строка %d.' % i.__add__(1))
                    words.append(get_word(row, user))
                # checking data: number of words
                elif len(row) != 0:
                    raise ValueError('Неправильный формат данных: число столбцов должно быть равно 7.', 'Строка %d.' % i.__add__(1))
    except Exception, e:
        # if we created words, we must remove them
        for word in words:
        	if word.created > now:
        		word.delete();
        raise e   
    return process_words(words)
                
def get_word(row, user):
    '''
    Each row contains following data:
    row[0] - signature; row[1] - translation;
    row[2] - speech part; row[3] - transcription;
    row[4] - synonyms; row[5] - sentences;
    row[7] - groups.
    Function returns new Word object with temp dictionary attribute 
    which contains synonyms, sentences and groups strings. 
    '''
    # silent checking speech part:
    # try to find similar speech part,
    # if no - get first
    try:
        sp = SpeechPart.objects.filter(name__contains=row[2])[0]
    except Exception, e:
        sp = SpeechPart.objects.all()[0] 
    # create word object
    words = Word.objects.filter(user=user, signature=row[0], speech_part=sp, translation=force_unicode(row[1]))
    if len(words) == 0:
    	word = Word.objects.create(user=user, 
                               signature=row[0], 
                               translation=force_unicode(row[1]),
                               speech_part=sp,
                               transcription=force_unicode(row[3]),
                               created=datetime.now())
    else:
    	word = words[0]
    # save synonyms, groups and sentences 
    # with word object for following processing
    word.temp = dict({'synonyms': row[4].strip(), 'sentences': force_unicode(row[5].strip()), 'groups': force_unicode(row[6].strip())})
    return word


def process_words(words):
    '''
    Function for processing synonyms, groups and sentences.
    '''
    for i, word in enumerate(words):
        process_synonyms(word, i)
        process_groups(word, i)
        process_sentences(word, i)
    return words

def process_synonyms(word, index=0):
    '''
    Function for processing synonyms in word.
    It adds only existent synonyms (words).
    '''
    if word.temp['synonyms']:
        for synonym in word.temp['synonyms'].split(', '):
            try:
                w = Word.objects.filter(user=word.user, signature=synonym, speech_part=word.speech_part)[0]
            except Exception, e:
                # Try to get phrase, verb synonyms.
                sp = None
                if word.speech_part.name == 'verb':
                    sp = SpeechPart.objects.get(name='phrase')
                elif word.speech_part.name == 'phrase':
                    sp = SpeechPart.objects.get(name='verb')
                if sp != None:
                    w = Word.objects.filter(user=word.user, signature=synonym, speech_part=sp)
                    if len(w) != 0:
                        w = w[0]
                    else:
                        w = None
                else:	
                    w = None
            if w != None:
                word.synonyms.add(w)

def process_groups(word, index=0):
    '''
    Function for processing groups.
    If such group doesn't exist, then create new one.
    :TODO: test ' ', '\r\n'
    ''' 
    if word.temp['groups']:
        for group in word.temp['groups'].split(', '):
            try:
                g = Group.objects.get(name=group, user=word.user)
            except Group.DoesNotExist, e:
                g = Group.objects.create(name=group, user=word.user, created=datetime.now())
            word.groups.add(g)

def process_sentences(word, index=0):
    '''    
    Function for processing sentences.
    If such sentence (body) doesn't exist, then create new.
    ''' 
    if word.temp['sentences']:
        for sentence in word.temp['sentences'].split(' | '):
            try:
                reg = re.match(r'^(?P<body>[^\[]+)(\[(?P<translation>.+)\])?$', sentence)
                (body, t, translation) = reg.groups()
                try:
                    s = Sentence.objects.get(body=body, user=word.user)
                except Sentence.DoesNotExist, e:
                    s = Sentence.objects.create(user=word.user, body=body, translation=translation, created=datetime.now())
                word.sentences.add(s)
            except Exception:
                pass



