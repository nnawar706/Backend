from django.contrib import admin

# Register your models here.
from .models import ExamRoom, ExamRoomHasStudents

admin.site.register(ExamRoom)
admin.site.register(ExamRoomHasStudents)