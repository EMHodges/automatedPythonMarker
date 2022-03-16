from django.urls import path

from .views import (question_list_view, question_update_views)

app_name = 'questions'

urlpatterns = [
    path('', question_list_view, name='question-list'),
    path('<int:number>/', question_update_views, name='question-update'),
]
