from django import forms
from django.forms.models import modelformset_factory

from . import models
from .fields import AnswerRadioSelect


class QuestionForm(forms.ModelForm):
    answer_options = forms.ModelChoiceField(
        widget=AnswerRadioSelect(),
        queryset=None,

    )

    class Meta:
        model = models.Question
        fields = ['answer_options']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer_options'].queryset = models.AnswerOption.objects.filter(question=self.instance)
        self.fields['answer_options'].label = "%s. %s" % (self.instance.number, self.instance.content)


# "extra=0" - remove create fields
QuestionFormSet = modelformset_factory(model=models.Question, form=QuestionForm, extra=0)
