from django.urls import path
from .views import ChildListCreate,MissionDetail,ChildProgress,SubmitQuiz
urlpatterns=[path('children/',ChildListCreate.as_view()),path('children/<int:child_id>/progress/',ChildProgress.as_view()),path('missions/<slug:slug>/',MissionDetail.as_view()),path('children/<int:child_id>/missions/<slug:slug>/submit/',SubmitQuiz.as_view())]
