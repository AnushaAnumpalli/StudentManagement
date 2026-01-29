from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.user_login, name='login'),   # root shows login page
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('home/', views.home, name='home'),

    # CRUD
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('toggle/<int:id>/', views.toggle_attendance, name='toggle_attendance'),
]