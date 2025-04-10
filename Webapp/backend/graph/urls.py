from django.urls import path
from .views import search_triples

urlpatterns = [
    path('triples/', search_triples),
]
