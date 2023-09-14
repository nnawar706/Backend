# Generated by Django 4.2.5 on 2023-09-14 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(blank=True, max_length=300, null=True)),
                ('total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(blank=True, max_length=100, null=True)),
                ('ques', models.CharField(max_length=1000)),
                ('sub_mark', models.FloatField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
            ],
        ),
        migrations.CreateModel(
            name='SubQuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000)),
                ('status', models.BooleanField()),
                ('sub_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.subquestion')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.questiontype'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz'),
        ),
    ]
