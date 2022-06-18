from django.urls import path
from dot import views
from django.views.generic import TemplateView

urlpatterns = [
    path('transfer/', views.transfer),
]