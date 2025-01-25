from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/image/<int:image_id>/delete/', views.delete_task_image, name='delete_task_image'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/toggle/<int:task_id>/', views.task_toggle, name='task_toggle'),
    path('tasks/lists/create/', views.task_list_create, name='task_list_create'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),    
    path("tasks/calendar-data/", views.calendar_data, name="calendar_data"),
    path('groups/', views.groups_list, name='groups_list'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('group/<int:pk>/edit/', views.edit_group, name='edit_group'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='board/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]
