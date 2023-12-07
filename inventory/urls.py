from django.urls import re_path as url
from .views import ReactAppView

urlpatterns = [
    #...
    url(r'^',ReactAppView.as_view()),
]