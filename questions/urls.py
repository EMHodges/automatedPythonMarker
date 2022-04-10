from django.urls import path

from .views import (question_list_view, question_update_views, question_generate_submission_file_view)

app_name = 'questions'

urlpatterns = [
    path('', question_list_view, name='question-list'),
    path('<int:number>/', question_update_views, name='question-update'),
    path('submit', question_generate_submission_file_view, name='question-submit')
]
