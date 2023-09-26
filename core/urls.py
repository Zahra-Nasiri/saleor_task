from django.urls import path
from .views import LogInUserView


urlpatterns = [
    path('login/',LogInUserView.as_view()),
]