from django.contrib import admin

from .models import *

admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(SubQuestion)
admin.site.register(SubQuestionAnswer)
