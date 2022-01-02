from django.urls import path
from .views import (question_update_view)

app_name = 'questions'

urlpatterns = [
    path('<int:number>/', question_update_view, name='question-update')
]
