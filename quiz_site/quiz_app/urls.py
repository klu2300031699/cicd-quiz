from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/start/', views.take_quiz, name='take_quiz'),
    path('results/', views.results_history, name='results_history'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/quizzes/', views.admin_quiz_list, name='admin_quiz_list'),
    path('admin-panel/quizzes/create/', views.admin_create_quiz, name='admin_create_quiz'),
    path('admin-panel/quizzes/<int:quiz_id>/edit/', views.admin_edit_quiz, name='admin_edit_quiz'),
    path('admin-panel/results/', views.admin_results, name='admin_results'),
    path('admin-panel/results/<int:attempt_id>/view/', views.admin_view_result, name='admin_view_result'),
]
