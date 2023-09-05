from django.urls import path
from .views import *

urlpatterns = [
    path("", ExamRoomsView.as_view()),
    path("store", ExamRoomsView.as_view()),
#     path("update", .as_view()),
#     path("delete", .as_view())
]