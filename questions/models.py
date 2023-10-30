from django.db import models
from quizzes.models import Quiz
from django.conf import settings

class QuestionType(models.Model):
    name           = models.CharField(max_length=50, unique = True)

    class Meta:
        db_table = 'question_types'

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz            = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type   = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    detail          = models.CharField(max_length=300, null=True, blank=True)
    total           = models.FloatField()

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.quiz.room.title + ' - ' + self.quiz.title + ' - ' + self.question_type.name


class SubQuestion(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='sub_questions')
    image_url       = models.CharField(max_length=100, null=True, blank=True)
    ques            = models.CharField(max_length=1000)
    sub_mark        = models.FloatField()

    class Meta:
        db_table = 'sub_questions'

    def __str__(self):
        return self.question.question_type.name + ' - ' + self.ques[:15] + '...'


class SubQuestionAnswer(models.Model):
    sub_question        = models.ForeignKey(SubQuestion, on_delete=models.CASCADE, related_name='answers')
    answer              = models.CharField(max_length=1000)
    status              = models.BooleanField()

    class Meta:
        db_table = 'sub_question_answers'

    def __str__(self):
        return self.sub_question.ques[:15] + '... - ' + self.answer[:10] + '...'


class SubQuestionMark (models.Model):
    student             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sq_marks')
    sub_question        = models.ForeignKey(SubQuestion, on_delete=models.CASCADE, related_name='marks')
    mark                = models.FloatField()

    class Meta:
        db_table = 'sub_question_marks'

    def __str__(self):
        return self.student.name + ' - ' + self.mark


class SubQuestionStudentAnswer (models.Model):
    sub_question_student_mark        = models.ForeignKey(SubQuestionMark, on_delete=models.CASCADE, related_name='student_answers')
    answer                             = models.ForeignKey(SubQuestionAnswer, on_delete=models.CASCADE, related_name='student_answers')

    class Meta:
        db_table = 'sub_question_student_answers'

    def __str__(self):
        return self.sub_question_student_answer.sub_question.id + ' - ' + self.answer