from django.contrib import admin

from .models import Question, AnswerOption


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    max_num = 2
    min_num = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerOptionInline,
    ]


admin.site.register(Question, QuestionAdmin)
