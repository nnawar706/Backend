# Generated by Django 4.2.5 on 2023-09-20 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_alter_quiz_room_quizmark'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizzes.quiz'),
        ),
        migrations.AlterField(
            model_name='subquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_questions', to='questions.question'),
        ),
        migrations.AlterField(
            model_name='subquestionanswer',
            name='sub_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questions.subquestion'),
        ),
    ]
