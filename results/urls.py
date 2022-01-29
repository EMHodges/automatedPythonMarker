from django.urls import path

from .views import (results_page_view)

app_name = 'results'

urlpatterns = [
    path('', results_page_view, name='results-page-view'),
]
