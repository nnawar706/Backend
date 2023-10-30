# Generated by Django 4.2.5 on 2023-10-25 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubQuestionStudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answers', to='questions.subquestionanswer')),
                ('sub_question_student_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answers', to='questions.subquestionmark')),
            ],
            options={
                'db_table': 'sub_question_student_answers',
            },
        ),
    ]
