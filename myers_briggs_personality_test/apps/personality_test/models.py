from django.db import models
from django.utils.translation import gettext_lazy as _


class DescriptorType(models.TextChoices):
    CONSCIOUSNESS_ORIENTATION = 'EI', _('Orientation of consciousness')         # Ориентация сознания (EI)
    SITUATION_ORIENTATION = 'SN', _('Orientation in the situation')             # Ориентация в ситуации (SN)
    DECISION_MAKING_BASIS = 'TF', _('The basis of decision-making')             # Основа принятия решений (TF)
    PREPARING_SOLUTIONS_METHOD = 'JP', _('The method of preparing solutions')   # Способ подготовки решений (JP)


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