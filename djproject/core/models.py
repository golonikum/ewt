# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
import re

def get_entity(cls):
    return  str(cls.__name__).lower()

def get_exercise_name():
    return re.sub(r'[\:\-\s]+', r'', unicode(datetime.now())[:-7])

class AjaxModel(models.Model):
    @classmethod
    @models.permalink
    def ajax_get_all(cls):
        return ('ajax_get_all', (), {'entity': get_entity(cls)})
    @models.permalink
    def ajax_get(self):
        return ('ajax_get', (), {'entity': get_entity(self.__class__), 'id': self.id})
    @classmethod
    @models.permalink
    def ajax_add(cls):
        return ('ajax_add', (), {'entity': get_entity(cls)})
    @models.permalink
    def ajax_update(self):
        return ('ajax_update', (), {'entity': get_entity(self.__class__), 'id': self.id})
    @models.permalink
    def ajax_remove(self):
        return ('ajax_remove', (), {'entity': get_entity(self.__class__), 'id': self.id})
    @classmethod
    @models.permalink
    def ajax_remove_some(cls):
        return ('ajax_remove_some', (), {'entity': get_entity(cls)})
    class Meta:
        abstract = True
        
class SpeechPart(models.Model):
    name = models.CharField(verbose_name=_('speech part'), max_length=40)    
    def __unicode__(self): return self.name
    def short_name(self):
		if self.name == 'verb':
			return 'v.'
		elif self.name == 'adjective':
			return 'adj.'
		elif self.name == 'noun':
			return 'n.'
		elif self.name == 'phrase':
			return 'phr.'
		elif self.name == 'adverb':
			return 'adv.'
		elif self.name == 'interjection':
			return 'int.'
		else:
			return self.name

class Group(AjaxModel):
    name = models.CharField(max_length=50, verbose_name=_('group'))
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    def __unicode__(self): return self.name
    class Meta:
        ordering = ['name']
    @models.permalink
    def ajax_change_words(self):
        return ('ajax_change_words', (), {'id': self.id, 'who': 'group'})

class Sentence(AjaxModel):
    body = models.TextField(max_length=255, verbose_name=_('sentence'))
    translation = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('translation'))
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    def __unicode__(self): return self.body
    class Meta:
        ordering = ['body']
    @models.permalink
    def ajax_change_words(self):
        return ('ajax_change_words', (), {'id': self.id, 'who': 'sentence'})

class Word(AjaxModel):
    signature = models.CharField(max_length=40, verbose_name=_('signature'))
    translation = models.TextField(max_length=300, verbose_name=_('translation'))
    transcription = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('transcription'))
    created = models.DateTimeField()
    user = models.ForeignKey(User)
    speech_part = models.ForeignKey(SpeechPart, verbose_name=_('speech part'))
    groups = models.ManyToManyField(Group, blank=True, null=True, verbose_name=_('groups'))
    synonyms = models.ManyToManyField('self', blank=True, null=True, verbose_name=_('synonyms'))
    sentences = models.ManyToManyField(Sentence, blank=True, null=True, verbose_name=_('sentences'))
    is_active = models.BooleanField(default=True, verbose_name=_('use in tests'))
    success = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    def __unicode__(self): 
    	if self.speech_part.name == 'verb':	
    		return 'to %s' % self.signature
    	else:
			return self.signature
    class Meta:
        ordering = ['signature']
    @models.permalink
    def ajax_change_synonyms(self):
        return ('ajax_change_word', (), {'id': self.id, 'what': 'synonyms'})
    @models.permalink
    def ajax_change_groups(self):
        return ('ajax_change_word', (), {'id': self.id, 'what': 'groups'})
    @models.permalink
    def ajax_change_sentences(self):
        return ('ajax_change_word', (), {'id': self.id, 'what': 'sentences'})
    
class ExerciseType(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500) 
    def __unicode__(self): return self.name

class Exercise(AjaxModel):
    title = models.CharField(max_length=100, verbose_name=_('title'), default=get_exercise_name())
    created = models.DateTimeField()
    finished = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User)
    from_date = models.DateField(blank=True, null=True, verbose_name=_('from date'))
    to_date = models.DateField(blank=True, null=True, verbose_name=_('to date'))
    speech_part = models.ForeignKey(SpeechPart, blank=True, null=True, verbose_name=_('speech part'))
    group = models.ForeignKey(Group, blank=True, null=True, verbose_name=_('group'))
    exercise_type = models.ForeignKey(ExerciseType, verbose_name=_('exercise type'))
    failed = models.IntegerField(blank=True, null=True, verbose_name=_('wrong more than'))
    def __unicode__(self): return self.title
    def get_success_num(self):
        return len(Record.objects.filter(exercise=self, is_passed=True))
    def get_failed_num(self):
        return len(Record.objects.filter(exercise=self, is_passed=False))
    @models.permalink
    def ajax_exercise(self):                         
        return ('ajax_exercise', (), {'id': self.id})
    @models.permalink
    def ajax_get_records(self):                         
        return ('ajax_get_records', (), {'id': self.id})
    
class Record(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    word = models.ForeignKey(Word)
    exercise = models.ForeignKey(Exercise)
    is_passed = models.BooleanField() 
    def __unicode__(self): return '%s: %s (%s)' % (self.timestamp, self.word, self.exercise)

class Config(models.Model):
    user = models.ForeignKey(User, unique=True)
    entities_per_page = models.IntegerField(default=15)
    def __unicode__(self): return '%s - %s' % (self.user.id, self.entities_per_page)

