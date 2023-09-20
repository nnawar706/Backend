from django.db import models
from django.conf import settings
from users.models import User

class ExamRoom(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='rooms')
    title       = models.CharField(max_length = 150)
    detail      = models.CharField(max_length = 300)
    secret      = models.CharField(max_length = 255)
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    students    = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student', through='ExamRoomHasStudents')

    class Meta:
        db_table = 'rooms'
        unique_together = ('user', 'title')

    def __str__(self):
        return self.user.name + ' - ' + self.title

class ExamRoomHasStudents(models.Model):
    room        = models.ForeignKey(ExamRoom, on_delete = models.CASCADE)
    student     = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'room_has_students'
        unique_together = ('room', 'student')

    def __str__(self):
        return self.room.title + ' - ' + self.student.name