from django.contrib import admin

from .models import ExamRoom, ExamRoomHasStudents

admin.site.register(ExamRoom)
admin.site.register(ExamRoomHasStudents)