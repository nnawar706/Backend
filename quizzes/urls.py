from django.urls import path
from .views import *

urlpatterns = [
    path("<int:room_id>", QuizCreateView.as_view()),
    path("all/<int:room_id>", QuizView.as_view()),
    path("update/<int:pk>", QuizUpdateView.as_view()),
    path("get_marks/<int:pk>", QuizMarksView.as_view()),
    path("publish_marks/<int:pk>", QuizMarksPublishView.as_view()),
]