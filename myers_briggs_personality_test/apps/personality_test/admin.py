import operator

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import (
    Question, 
    AnswerOption, 
    DescriptorInfo, 
    UserResult, 
    UserResponseQuestion, 
    DescriptorType
)
from .utils import calculate_test_result_by_descriptor_type, get_user_result_answers


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    max_num = 2
    min_num = 2
    can_delete = False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline,]


class UserResponseQuestionInline(admin.StackedInline):
    model = UserResponseQuestion
    can_delete = False
    max_num = 0
    fields = ('number', 'answer_content', 'answer_result')
    readonly_fields = ('number', 'answer_content', 'answer_result')

    def number(self, obj):
        return obj.answer.question.number

    def answer_result(self, obj):
        if obj.answer_descriptor_type == 'nan':
            return '-'
        return "%s (+%s)" % (obj.get_answer_descriptor_type_display(), obj.answer_descriptor_count)


@admin.register(UserResult)
class UserResultAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'descriptor_info', 'created_at')
    fieldsets = (
        (None, {"fields": ('user_name', 'user_email',)}),
        (_("Descriptor info"), {"fields": ('descriptor_info_abbr', 'descriptor_info_name', 'user_result_list')}),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),
    )
    inlines = [UserResponseQuestionInline,]

    def descriptor_info_abbr(self, obj):
        return obj.descriptor_info

    def descriptor_info_name(self, obj):
        return obj.descriptor_info.name

    def user_result_list(self, obj):
        """        
        7 это E(3)    
        12 это S    (4)
        12 это T (5)
        15  -    J  (6)
        итого 49 / 70 (7)
        """
        user_result_answers = get_user_result_answers(obj)

        user_result_html = ""
        user_result_full = (0, 0)
        for descriptor_type_str, (user_result, max_result, descriptor_type_item) in user_result_answers.items():
            user_result_html += "%s of %s (%s)<br>" % (user_result, max_result, descriptor_type_item)
            user_result_full = tuple(map(operator.add, user_result_full, (user_result, max_result)))

        user_result_html += "Total: %s of %s" % (*user_result_full, )
        return mark_safe(user_result_html)

    def get_readonly_fields(self, request, obj=None):
        """
        All fields are readonly
        """
        return ('user_name', 'user_email', 'descriptor_info', 'created_at', 'updated_at', 
                'descriptor_info_abbr', 'descriptor_info_name', 'user_result_list')


admin.site.register(DescriptorInfo)