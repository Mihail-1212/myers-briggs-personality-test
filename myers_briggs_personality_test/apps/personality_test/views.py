from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from . import models, forms
from .utils import get_descriptor_info_by_test


def index_page(request):
    return render(request, "personality_test/index_page.html", context={})


class PersonalityTestView(View):
    model = models.Question
    template_name = "personality_test/personality_test_page.html"

    def get_question_queryset(self):
        return self.model.objects.all()

    def get(self, request):
        """
        GET method
        return list of questions with options
        """
        # Get form test
        test_form = forms.TestForm()
        # Get formset from queryset
        question_forms = forms.QuestionFormSet(queryset=self.get_question_queryset())
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
        # Get formset from request
        question_forms = forms.QuestionFormSet(data=request.POST, queryset=self.get_question_queryset())

        if test_form.is_valid() and question_forms.is_valid():
            # Init user result model objs
            user_result = test_form.save(commit=False)
            user_responses = []
            # Generate dict with models.DescriptorType:0
            test_result = {choice: 0 for choice in models.DescriptorType}
            for record in question_forms.cleaned_data:
                answer = record['answer_options']
                descriptor_weight = answer.descriptor_count
                user_responses.append(models.UserResponseQuestion(user_result=user_result, answer=answer))
                try:
                    descriptor_type = models.DescriptorType(answer.descriptor_increase)
                except ValueError:
                    # If descriptor_type is not a valid DescriptorType or is Null
                    continue
                test_result[descriptor_type] += descriptor_weight

            descriptor_info = get_descriptor_info_by_test(test_result)
            user_result.descriptor_info = descriptor_info

            # TODO: try-catch
            try:
                user_result.save()
                models.UserResponseQuestion.objects.bulk_create(user_responses)
            except Exception:
                pass

            # Add message to page
            messages.info(request, _('User %(user)s with email %(email)s, this is page of your type') % {
                'user': user_result.user_name,
                'email': user_result.user_email
            })
            messages.info(request, _('Your type is %(type)s') % {'type': descriptor_info})
            # Redirect to page
            return redirect(descriptor_info)

        # Render page
        return render(request, self.template_name, context={
            'test_form': test_form,
            'question_forms': question_forms
        })


class DescriptorListView(ListView):
    model = models.DescriptorInfo
    context_object_name = 'descriptor_list'
    template_name = 'personality_test/descriptor_list.html'


class DescriptorDetailView(DetailView):
    model = models.DescriptorInfo
    pk_url_kwarg = 'descriptor_id'
    template_name = 'personality_test/descriptor_detail.html'
    context_object_name = 'descriptor_object'

