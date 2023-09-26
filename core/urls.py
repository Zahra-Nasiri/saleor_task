from django.urls import path
from .views import LogInUserView, CategoryView


urlpatterns = [
    path('login/',LogInUserView.as_view()),
    path('category/', CategoryView.as_view()),
]