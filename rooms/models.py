from django.db import models
from django.conf import settings

class ExamRoom(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title       = models.CharField(max_length = 150)
    detail      = models.CharField(max_length = 300)
    secret      = models.CharField(max_length = 255)
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return self.user.name + ' - ' + self.title