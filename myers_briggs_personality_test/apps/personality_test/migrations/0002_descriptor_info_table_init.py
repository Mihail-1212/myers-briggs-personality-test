# Generated by Django 3.2.18 on 2023-03-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personality_test', '0001_init_question_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeroption',
            name='descriptor_increase',
            field=models.CharField(blank=True, choices=[('EI', 'Orientation of consciousness'), ('SN', 'Orientation in the situation'), ('TF', 'The basis of decision-making'), ('JP', 'The method of preparing solutions')], max_length=50, verbose_name='descriptor type to increase'),
        ),
        migrations.CreateModel(
            name='DescriptorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consciousness_orientation', models.BooleanField(default=False, help_text='False - I, True - E', verbose_name='Orientation of consciousness')),
                ('situation_orientation', models.BooleanField(default=False, help_text='False - N, True - S', verbose_name='Orientation in the situation')),
                ('decision_making_basis', models.BooleanField(default=False, help_text='False - F, True - T', verbose_name='The basis of decision-making')),
                ('preparing_solutions_method', models.BooleanField(default=False, help_text='False - P, True - J', verbose_name='The method of preparing solutions')),
                ('name', models.CharField(max_length=50, verbose_name='descriptor name')),
                ('name_decoding', models.CharField(max_length=100, verbose_name='decoding of descriptor name')),
                ('full_description', models.TextField(verbose_name='full description')),
            ],
            options={
                'verbose_name': 'descriptor info',
                'verbose_name_plural': 'descriptor info',
                'unique_together': {('consciousness_orientation', 'situation_orientation', 'decision_making_basis', 'preparing_solutions_method')},
            },
        ),
    ]