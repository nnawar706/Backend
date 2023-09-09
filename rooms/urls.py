from django.urls import path
from .views import *

urlpatterns = [
    path("", ExamRoomsView.as_view()),
    path("<int:pk>", .as_view())
]