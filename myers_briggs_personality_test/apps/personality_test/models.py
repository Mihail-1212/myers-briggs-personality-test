from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserResponseQuestionManager


class DescriptorType(models.TextChoices):
    CONSCIOUSNESS_ORIENTATION = 'EI', _('Orientation of consciousness')         # Ориентация сознания (EI)
    SITUATION_ORIENTATION = 'SN', _('Orientation in the situation')             # Ориентация в ситуации (SN)
    DECISION_MAKING_BASIS = 'TF', _('The basis of decision-making')             # Основа принятия решений (TF)
    PREPARING_SOLUTIONS_METHOD = 'JP', _('The method of preparing solutions')   # Способ подготовки решений (JP)


class DescriptorInfo(models.Model):
    consciousness_orientation = models.BooleanField(default=False, verbose_name='Orientation of consciousness',
                                                    help_text=_('False - I, True - E'))
    situation_orientation = models.BooleanField(default=False, verbose_name='Orientation in the situation',
                                                help_text=_('False - N, True - S'))
    decision_making_basis = models.BooleanField(default=False, verbose_name='The basis of decision-making',
                                                help_text=_('False - F, True - T'))
    preparing_solutions_method = models.BooleanField(default=False, verbose_name='The method of preparing solutions',
                                                     help_text=_('False - P, True - J'))

    name = models.CharField(max_length=50, verbose_name=_('descriptor name'))
    name_decoding = models.CharField(max_length=100, verbose_name=_('decoding of descriptor name'))
    full_description = models.TextField(blank=False, verbose_name=_('full description'))

    class Meta:
        verbose_name = _('descriptor info')
        verbose_name_plural = _('descriptor info')
        unique_together = ('consciousness_orientation', 'situation_orientation',
                           'decision_making_basis', 'preparing_solutions_method')

    def get_absolute_url(self):
        return reverse("descriptor_detail", kwargs={"descriptor_id": self.id})

    def get_consciousness_orientation(self):
        return 'E' if self.consciousness_orientation else 'I'

    def get_situation_orientation(self):
        return 'S' if self.situation_orientation else 'N'

    def get_decision_making_basis(self):
        return 'T' if self.decision_making_basis else 'F'

    def get_preparing_solutions_method(self):
        return 'J' if self.preparing_solutions_method else 'P'

    def __str__(self):
        """
        String type of "ESTJ"
        """
        return "%s%s%s%s" % (self.get_consciousness_orientation(), self.get_situation_orientation(),
                             self.get_decision_making_basis(), self.get_preparing_solutions_method())


class Question(models.Model):
    number = models.IntegerField(blank=True, unique=True, verbose_name=_('number of question'))
    content = models.TextField(max_length=400, blank=False, verbose_name=_('content of question'))

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ['number']
        get_latest_by = 'number'

    def save(self, *args, **kwargs):
        """
        Save the current instance.
        On creation set number (max number + 1) if field is blank
        """
        if not self.id and not self.number:
            try:
                # Get max question by number and increase it
                self.number = Question.objects.latest().number + 1
            except Question.DoesNotExist:
                self.number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "(%s) %s" % (self.number, self.content)

    @classmethod
    def get_max_weight_descriptor_type(cls, descriptor_type):
        """
        Return max weight of given "descriptor_type" var
        """
        assert isinstance(descriptor_type, DescriptorType),\
            '"descriptor_type" variable must be "DescriptorType" type'

        question_objs = cls.objects.filter(answer_options__descriptor_increase=descriptor_type)

        max_weight = 0
        for question in question_objs:
            answer_obj = question.answer_options.filter(descriptor_increase=descriptor_type).\
                order_by('-descriptor_count').first()
            max_weight += answer_obj.descriptor_count
        return max_weight


class AnswerOption(models.Model):
    answer_text = models.CharField(max_length=200, verbose_name=_('answer text'))
    descriptor_count = models.IntegerField(blank=False, default=1, verbose_name=_('descriptor count number'))
    descriptor_increase = models.CharField(max_length=50, blank=True, choices=DescriptorType.choices,
                                           verbose_name=_('descriptor type to increase'))

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('question'),
                                 related_name='answer_options')

    class Meta:
        verbose_name = _('answer option')
        verbose_name_plural = _('answer options')

    def __str__(self):
        return "%s" % self.answer_text


class UserResult(models.Model):
    user_name = models.CharField(max_length=150, verbose_name=_('user name'))
    user_email = models.EmailField(verbose_name=_('user email address'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    descriptor_info = models.ForeignKey(DescriptorInfo, on_delete=models.CASCADE, verbose_name=_('descriptor info'),
                                        related_name='user_results')

    class Meta:
        verbose_name = _('user result')
        verbose_name_plural = _('user results')

    def __str__(self):
        return "%s (%s)" % (self.user_name, self.user_email)

    @transaction.atomic
    def save_create_user_responses(self, user_responses):
        """
        Save instance of user result and create user responses for this instance
        and return boolean result of save operation
        """
        for user_response in user_responses:
            user_response.user_result = self
        # Set transaction point
        sid = transaction.savepoint()
        # Save current instance
        try:
            self.save()
            UserResponseQuestion.objects.bulk_create(user_responses)
            transaction.savepoint_commit(sid)
        except Exception:
            # Rollback on error
            transaction.savepoint_rollback(sid)
            return False
        return True


class UserResponseQuestion(models.Model):
    # Override object manager for current model
    objects = UserResponseQuestionManager()

    question_content = models.TextField(blank=True, max_length=400, verbose_name=_('content of question'))
    answer_content = models.TextField(blank=True, max_length=400, verbose_name=_('content of question'))
    answer_descriptor_count = models.IntegerField(blank=True, verbose_name=_('descriptor count number'))
    answer_descriptor_type = models.CharField(blank=True, max_length=50, choices=DescriptorType.choices,
                                              verbose_name=_('descriptor type to increase'))

    answer = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('answer'),
                               related_name='user_responses')
    user_result = models.ForeignKey(UserResult, on_delete=models.CASCADE, verbose_name=_('user response to question'),
                                    related_name='user_responses')

    class Meta:
        verbose_name = _('user response to question')
        verbose_name_plural = _('user responses to question')

    def __str__(self):
        return "%s" % (self.answer.question.content, )

