import pandas as pd
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from personality_test.models import Question, AnswerOption


class Command(BaseCommand):
    help = 'Load question dummy data'

    def handle(self, *args, **options):
        dummy_file_name = 'data.csv'
        commands_directory = os.path.join(Path(__file__).resolve().parent.parent, 'dummy')
        dummy_file_path = os.path.join(commands_directory, dummy_file_name)

        dummy_question_count = 0
        df = pd.read_csv(dummy_file_path, sep=';', header=0, encoding='utf-8').to_dict(orient='records')
        for row in df:
            record_dict = row
            try:
                question = Question(number=int(record_dict['question_number']), content=record_dict['question_content'])
                question.save()
                # Create 2 answers
                AnswerOption.objects.create(answer_text=record_dict['answer_1_text'],
                                            descriptor_count=int(record_dict['answer_1_weigth']),
                                            descriptor_increase=record_dict['answer_1_descriptor'],
                                            question=question)
                AnswerOption.objects.create(answer_text=record_dict['answer_2_text'],
                                            descriptor_count=int(record_dict['answer_2_weigth']),
                                            descriptor_increase=record_dict['answer_2_descriptor'],
                                            question=question)
                dummy_question_count += 1
            except IntegrityError as exception:
                self.stdout.write(self.style.ERROR("%s number record already exist" % int(record_dict['question_number'])))
                continue
            except ValueError as exception:
                # If record hav NAN value
                break

        self.stdout.write(self.style.SUCCESS('Successfully created %s questions' % dummy_question_count))
