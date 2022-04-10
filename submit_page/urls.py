from django.urls import path

from .views import (submit_view)

app_name = 'submit_page'

urlpatterns = [
    path('submit_view/', submit_view, name='submit-view'),
]
