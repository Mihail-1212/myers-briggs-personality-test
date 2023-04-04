from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import gettext_lazy as _

from . import models
from .fields import AnswerRadioSelect


class TestForm(forms.ModelForm):
    class Meta:
        model = models.UserResult
        fields = ['user_name', 'user_email']
        help_texts = {
            'user_name': _("Enter your name"),
            'user_email': _("Enter your contact email"),
        }

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        # Add bootstrap "form-control" class to inputs
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class QuestionForm(forms.ModelForm):
    answer_options = forms.ModelChoiceField(
        widget=AnswerRadioSelect(),
        queryset=None,
        required=True
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
