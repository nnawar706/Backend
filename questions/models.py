from django.db import models
from quizzes.models import Quiz

class QuestionType(models.Model):
    name           = models.CharField(max_length=50, unique = True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz            = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type   = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    detail          = models.CharField(max_length=300, null=True, blank=True)
    total           = models.FloatField()

    def __str__(self):
        return self.quiz.room.title + ' - ' + self.quiz.title + ' - ' + self.question_type.name


class SubQuestion(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    image_url       = models.CharField(max_length=100, null=True, blank=True)
    ques            = models.CharField(max_length=1000)
    sub_mark        = models.FloatField()

    def __str__(self):
        return self.question.question_type.name + ' - ' + self.ques[:15] + '...'


class SubQuestionAnswer(models.Model):
    sub_question        = models.ForeignKey(SubQuestion, on_delete=models.CASCADE)
    answer              = models.CharField(max_length=1000)
    status              = models.BooleanField()

    def __str__(self):
        return self.sub_question.ques[:15] + '... - ' + self.answer[:10] + '...'