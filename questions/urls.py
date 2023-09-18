from django.urls import path
from .views import *

urlpatterns = [
    path("", QuestionCreateView.as_view()),
    path("<int:quiz_id>", QuestionView.as_view()),
    path("pdf/<int:quiz_id>", QuestionPdfView.as_view()),
#     path("send_invitation/<int:pk>", SendJoiningInvitationView.as_view()),
#     path("join_room", JoinExamRoomView.as_view()),
]