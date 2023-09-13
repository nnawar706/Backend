from django.urls import path
from .views import *

urlpatterns = [
    path("<int:room_id>", QuizCreateView.as_view()),
#     path("<int:pk>", RetrieveExamRoomView.as_view()),
#     path("send_invitation/<int:pk>", SendJoiningInvitationView.as_view()),
#     path("join_room", JoinExamRoomView.as_view()),
]