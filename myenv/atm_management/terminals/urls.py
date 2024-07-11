from django.urls import path
from . import views

urlpatterns = [
    path('', views.terminal_list, name='terminal_list'),
    path('terminal/<int:pk>/', views.terminal_detail, name='terminal_detail'),
    path('terminal/new/', views.terminal_new, name='terminal_new'),
    path('terminal/<int:pk>/edit/', views.terminal_edit, name='terminal_edit'),
    path('terminal/new/', views.terminal_new, name='terminal_new'),
]
