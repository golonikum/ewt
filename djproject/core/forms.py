from django import forms
from core.models import Word, Group, Sentence, Exercise, SpeechPart
from django.utils.translation import gettext_lazy as _

def _blank_choice_label():
    return _('Select an option')

def _localize_empty_labels(form):
    label = _blank_choice_label()
    for field in form.fields.values():
        if getattr(field, 'empty_label', None) not in (None, False):
            field.empty_label = label


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        exclude = ('groups', 'synonyms', 'sentences', 'created', 'user', 'success', 'failed')
    def __init__(self, user, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(WordForm, self).__init__(*args, **kwargs)
        _localize_empty_labels(self)
    	
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = ('created', 'user', 'finished')
    def __init__(self, user, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ExerciseForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)
        _localize_empty_labels(self)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', )
    def __init__(self, user, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(GroupForm, self).__init__(*args, **kwargs)
  
class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ('body', 'translation')
    def __init__(self, user, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SentenceForm, self).__init__(*args, **kwargs)

class ExportForm(forms.Form):
    groups = forms.MultipleChoiceField(required=False, label=_('Groups'))
    speechparts = forms.MultipleChoiceField(required=False, label=_('Speech Parts'))
    from_date = forms.DateField(required=False, label=_('From Date'))
    to_date = forms.DateField(required=False, label=_('To Date'))
    def __init__(self, user, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['groups'].choices = Group.objects.filter(user=user).values_list('id', 'name')
        self.fields['speechparts'].choices = SpeechPart.objects.values_list('id', 'name')
