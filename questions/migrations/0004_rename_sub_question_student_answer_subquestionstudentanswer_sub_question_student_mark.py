# Generated by Django 4.2.5 on 2023-10-30 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_subquestionstudentanswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subquestionstudentanswer',
            old_name='sub_question_student_answer',
            new_name='sub_question_student_mark',
        ),
    ]
