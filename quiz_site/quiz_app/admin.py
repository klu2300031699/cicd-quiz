from django.contrib import admin
from .models import UserProfile, Quiz, Question, UserQuizAttempt

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total_quizzes_attempted']
    search_fields = ['user__username', 'user__email']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'quiz_type', 'num_questions', 'total_questions', 'time_limit', 'is_active', 'created_at']
    list_filter = ['quiz_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text', 'correct_option', 'created_at']
    list_filter = ['quiz', 'correct_option']
    search_fields = ['text']

@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'date_attempted']
    list_filter = ['quiz', 'date_attempted']
    search_fields = ['user__username', 'quiz__name']
    date_hierarchy = 'date_attempted'
