from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext_lazy as _

from . import models, forms


class PersonalityTestView(View):
    model = models.Question
    template_name = "personality_test/personality_test_page.html"

    def get(self, request):
        """
        GET method
        return list of questions with options
        """
        # Get queryset
        question_list = self.model.objects.all()
        # Get formset from queryset
        question_forms = forms.QuestionFormSet(queryset=question_list)

        # Render page
        return render(request, self.template_name, context={
            'question_list': question_list,
            'question_forms': question_forms
        })

    def post(self, request):
        """
        POST method
        Process answers and return test result
        """
        pass

