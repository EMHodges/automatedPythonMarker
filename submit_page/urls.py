from django.urls import path

from .views import (submit_view, submit_page)

app_name = 'submit_page'

urlpatterns = [
    path('', submit_page, name='submit-page'),
    path('submit_view/', submit_view, name='submit-view'),
]
