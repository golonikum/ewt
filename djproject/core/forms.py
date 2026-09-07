from django import forms
from core.models import Word, Group, Sentence, Exercise, SpeechPart
from django.utils.translation import ugettext_lazy as _

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        exclude = ('groups', 'synonyms', 'sentences', 'created', 'user', 'success', 'failed')
    def __init__(self, user, *args, **kwargs):
        super(WordForm, self).__init__(*args, **kwargs)
    	
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = ('created', 'user', 'finished')
    def __init__(self, user, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', )
    def __init__(self, user, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
  
class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ('body', 'translation')
    def __init__(self, user, *args, **kwargs):
        super(SentenceForm, self).__init__(*args, **kwargs)

class ExportForm(forms.Form):
    groups = forms.MultipleChoiceField(required=False, label=_('Groups'))
    speechparts = forms.MultipleChoiceField(required=False, label=_('Speech Parts'))
    from_date = forms.DateField(required=False, label=_('From Date'))
    to_date = forms.DateField(required=False, label=_('To Date'))
    def __init__(self, user, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['groups'].choices = Group.objects.filter(user=user).values_list('id', 'name')
        self.fields['speechparts'].choices = SpeechPart.objects.values_list('id', 'name')
