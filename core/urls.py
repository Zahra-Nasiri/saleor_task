from django.urls import path
from .views import LogInUserView, CategoryView, ProductsView


urlpatterns = [
    path('login/',LogInUserView.as_view()),
    path('category/', CategoryView.as_view()),
    path('product/', ProductsView.as_view()),
]