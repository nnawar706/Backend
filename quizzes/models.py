from django.db import models
from rooms.models import ExamRoom

class Quiz(models.Model):
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