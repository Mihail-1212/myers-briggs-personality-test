from django.db import models


class UserResponseQuestionManager(models.Manager):
	def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
		"""
		Insert each of the instances into the database
		"""
		for obj in objs:
			obj.question_content = obj.answer.question.content
			obj.answer_content = obj.answer.answer_text
			obj.answer_descriptor_count = obj.answer.descriptor_count
			obj.answer_descriptor_type = obj.answer.descriptor_increase
		super().bulk_create(objs, batch_size, ignore_conflicts)