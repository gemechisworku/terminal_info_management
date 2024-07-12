from django.urls import path
from . import views

urlpatterns = [
    path('', views.terminal_list, name='terminal_list'),
    path('terminal/<int:pk>/', views.terminal_detail, name='terminal_detail'),
    path('terminal/new/', views.terminal_new, name='terminal_new'),
    path('terminal/<int:pk>/edit/', views.terminal_edit, name='terminal_edit'),
    path('port_assignment/', views.port_assignment, name='port_assignment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('terminals/ncr', views.ncr_terminals, name='ncr_terminals'),
    path('terminals/hitachi_crm', views.hitachi_crm_terminals, name='hitachi_crm_terminals'),
    path('terminals/pos', views.pos_terminals, name='pos_terminals'),
    path('terminals/<str:terminal_type>/', views.terminal_list_by_type, name='terminal_list_by_type'),  # New URL pattern for different terminal types
]
