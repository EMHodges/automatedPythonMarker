from django.urls import path

from .views import (question_list_view, question_update_view, submit_view)

app_name = 'questions'

urlpatterns = [
    path('', question_list_view, name='question-list'),
    path('<int:number>/', question_update_view, name='question-update'),
    path('submit', submit_view, name='question-submit')
]
