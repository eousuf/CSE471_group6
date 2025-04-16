from django.urls import path
from .views import register_child

urlpatterns = [
    path('register/', register_child, name='children_register'),
]
