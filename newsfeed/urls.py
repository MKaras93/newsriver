from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.display_articles_set, name='Fresh articles'),
    path('<query>', views.display_articles_set)
]