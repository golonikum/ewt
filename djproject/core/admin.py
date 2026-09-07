# coding=utf-8
from core.models import Word, Group, SpeechPart, Sentence, Exercise, ExerciseType, Record, Config
from django.contrib import admin

admin.site.register(Word)
admin.site.register(Group)
admin.site.register(SpeechPart)
admin.site.register(Sentence)
admin.site.register(Exercise)
admin.site.register(ExerciseType)
admin.site.register(Record)
admin.site.register(Config)
