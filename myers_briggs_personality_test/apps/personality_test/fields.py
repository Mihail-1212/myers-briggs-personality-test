from django.forms import RadioSelect


class AnswerRadioSelect(RadioSelect):
    option_template_name = "personality_test/forms/answer_option.html"
