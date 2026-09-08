# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import re

def get_entity(cls):
    return  str(cls.__name__).lower()

def get_exercise_name():
    return re.sub(r'[\:\-\s]+', r'', str(datetime.now())[:-7])

class AjaxModel(models.Model):
    @classmethod
    def ajax_get_all(cls):
        return reverse('ajax_get_all', kwargs={'entity': get_entity(cls)})
    def ajax_get(self):
        return reverse('ajax_get', kwargs={'entity': get_entity(self.__class__), 'id': self.id})
    @classmethod
    def ajax_add(cls):
        return reverse('ajax_add', kwargs={'entity': get_entity(cls)})
    def ajax_update(self):
        return reverse('ajax_update', kwargs={'entity': get_entity(self.__class__), 'id': self.id})
    def ajax_remove(self):
        return reverse('ajax_remove', kwargs={'entity': get_entity(self.__class__), 'id': self.id})
    @classmethod
    def ajax_remove_some(cls):
        return reverse('ajax_remove_some', kwargs={'entity': get_entity(cls)})
    class Meta:
        abstract = True

class SpeechPart(models.Model):
    name = models.CharField(verbose_name=_('speech part'), max_length=40)
    def __str__(self): return self.name
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField()
    def __str__(self): return self.name
    class Meta:
        ordering = ['name']
    def ajax_change_words(self):
        return reverse('ajax_change_words', kwargs={'id': self.id, 'who': 'group'})

class Sentence(AjaxModel):
    body = models.TextField(max_length=255, verbose_name=_('sentence'))
    translation = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('translation'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField()
    def __str__(self): return self.body
    class Meta:
        ordering = ['body']
    def ajax_change_words(self):
        return reverse('ajax_change_words', kwargs={'id': self.id, 'who': 'sentence'})

class Word(AjaxModel):
    signature = models.CharField(max_length=40, verbose_name=_('signature'))
    translation = models.TextField(max_length=300, verbose_name=_('translation'))
    transcription = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('transcription'))
    created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speech_part = models.ForeignKey(SpeechPart, on_delete=models.CASCADE, verbose_name=_('speech part'))
    groups = models.ManyToManyField(Group, blank=True, verbose_name=_('groups'))
    synonyms = models.ManyToManyField('self', blank=True, verbose_name=_('synonyms'))
    sentences = models.ManyToManyField(Sentence, blank=True, verbose_name=_('sentences'))
    is_active = models.BooleanField(default=True, verbose_name=_('use in tests'))
    success = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    def __str__(self):
        if self.speech_part.name == 'verb':
            return 'to %s' % self.signature
        else:
            return self.signature
    class Meta:
        ordering = ['signature']
    def ajax_change_synonyms(self):
        return reverse('ajax_change_word', kwargs={'id': self.id, 'what': 'synonyms'})
    def ajax_change_groups(self):
        return reverse('ajax_change_word', kwargs={'id': self.id, 'what': 'groups'})
    def ajax_change_sentences(self):
        return reverse('ajax_change_word', kwargs={'id': self.id, 'what': 'sentences'})

class ExerciseType(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    def __str__(self): return self.name

class Exercise(AjaxModel):
    # Callable default: calling it here would freeze one timestamp into the
    # migration and regenerate it on every makemigrations run.
    title = models.CharField(max_length=100, verbose_name=_('title'), default=get_exercise_name)
    created = models.DateTimeField()
    finished = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField(blank=True, null=True, verbose_name=_('from date'))
    to_date = models.DateField(blank=True, null=True, verbose_name=_('to date'))
    speech_part = models.ForeignKey(SpeechPart, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('speech part'))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('group'))
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, verbose_name=_('exercise type'))
    failed = models.IntegerField(blank=True, null=True, verbose_name=_('wrong more than'))
    def __str__(self): return self.title
    def get_success_num(self):
        return len(Record.objects.filter(exercise=self, is_passed=True))
    def get_failed_num(self):
        return len(Record.objects.filter(exercise=self, is_passed=False))
    def ajax_exercise(self):
        return reverse('ajax_exercise', kwargs={'id': self.id})
    def ajax_get_records(self):
        return reverse('ajax_get_records', kwargs={'id': self.id})

class Record(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_passed = models.BooleanField()
    def __str__(self): return '%s: %s (%s)' % (self.timestamp, self.word, self.exercise)

class Config(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entities_per_page = models.IntegerField(default=15)
    def __str__(self): return '%s - %s' % (self.user.id, self.entities_per_page)
