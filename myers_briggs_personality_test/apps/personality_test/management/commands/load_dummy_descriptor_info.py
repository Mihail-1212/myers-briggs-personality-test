import pandas as pd
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from personality_test.models import DescriptorInfo


class Command(BaseCommand):
    help = 'Load question dummy data'

    def handle(self, *args, **options):
        dummy_file_name = 'descriptor.csv'
        commands_directory = os.path.join(Path(__file__).resolve().parent.parent, 'dummy')
        dummy_file_path = os.path.join(commands_directory, dummy_file_name)

        dummy_descriptor_count = 0
        df = pd.read_csv(dummy_file_path, sep=';', header=0, encoding='utf-8').to_dict(orient='records')
        for row in df:
            record_dict = row
            try:
                descriptor_record = DescriptorInfo(
                    consciousness_orientation=bool(record_dict['consciousness_orientation']),
                    situation_orientation=bool(record_dict['situation_orientation']),
                    decision_making_basis=bool(record_dict['decision_making_basis']),
                    preparing_solutions_method=bool(record_dict['preparing_solutions_method']),
                    name=record_dict['name'],
                    name_decoding=record_dict['name_decoding'],
                    full_description=record_dict['full_description'],
                )
                descriptor_record.save()
                dummy_descriptor_count += 1
            except IntegrityError as exception:
                self.stdout.write(self.style.ERROR("%s already exist" % descriptor_record))
                continue
            except ValueError as exception:
                # If record hav NAN value
                break

        self.stdout.write(self.style.SUCCESS('Successfully created %s records' % dummy_descriptor_count))
