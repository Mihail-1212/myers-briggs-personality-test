from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from . import models, forms


def index_page(request):
    return render(request, "personality_test/index_page.html", context={})


class PersonalityTestView(View):
    model = models.Question
    template_name = "personality_test/personality_test_page.html"

    def get(self, request):
        """
        GET method
        return list of questions with options
        """
        # Get form test
        test_form = forms.TestForm()
        # Get queryset
        question_list = self.model.objects.all()
        # Get formset from queryset
        question_forms = forms.QuestionFormSet(queryset=question_list)

        # Render page
        return render(request, self.template_name, context={
            'test_form': test_form,
            'question_forms': question_forms
        })

    def post(self, request):
        """
        POST method
        Process answers and return test result
        """
        # Get form test
        test_form = forms.TestForm(data=request.POST)
        # Get formset from queryset
        question_forms = forms.QuestionFormSet(data=request.POST)
        if test_form.is_valid() and question_forms.is_valid():
            # process form data
            # redirect to page of descriptor
            return
        return


class DescriptorListView(ListView):
    model = models.DescriptorInfo
    context_object_name = 'descriptor_list'
    template_name = 'personality_test/descriptor_list.html'


class DescriptorDetailView(DetailView):
    model = models.DescriptorInfo
    pk_url_kwarg = 'descriptor_id'
    template_name = 'personality_test/descriptor_detail.html'
    context_object_name = 'descriptor_object'

