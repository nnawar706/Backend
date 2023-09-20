from django.db import models
from rooms.models import ExamRoom
from django.conf import settings

class Quiz (models.Model):
    room            = models.ForeignKey(ExamRoom, on_delete=models.CASCADE, related_name='quizzes')
    title           = models.CharField(max_length=50)
    occurring_date  = models.DateField()
    from_time       = models.TimeField()
    to_time         = models.TimeField()
    total_marks     = models.IntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'title')

    def __str__(self):
        return self.room.title + ' - ' + self.title


class QuizMark (models.Model):
    quiz          = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz')
    student       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='examinee')
    obtained_mark = models.FloatField()

    class Meta:
        unique_together = ('quiz', 'student')

    def __str__(self):
        return self.quiz.room.title + ' - ' + self.quiz.title + ' - ' + self.obtained_mark