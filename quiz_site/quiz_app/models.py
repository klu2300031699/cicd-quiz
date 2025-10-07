from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def total_quizzes_attempted(self):
        return UserQuizAttempt.objects.filter(user=self.user).count()

class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('random', 'Random'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.IntegerField(help_text="Time limit in minutes")
    num_questions = models.IntegerField(help_text="Number of questions to show to user")
    total_questions = models.IntegerField(help_text="Total questions available in the quiz")
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES, default='fixed')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
    
    def __str__(self):
        return self.name
    
    def get_questions(self):
        """Get questions for this quiz based on quiz type"""
        questions = self.questions.all()
        if self.quiz_type == 'random' and questions.count() >= self.num_questions:
            return questions.order_by('?')[:self.num_questions]
        return questions[:self.num_questions]

class Question(models.Model):
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quiz.name} - {self.text[:50]}"
    
    def get_correct_answer_text(self):
        """Return the text of the correct option"""
        option_map = {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }
        return option_map.get(self.correct_option, '')

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField()
    date_attempted = models.DateTimeField(default=timezone.now)
    user_answers = models.JSONField(default=dict)
    correct_answers = models.JSONField(default=dict)
    questions_data = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-date_attempted']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.name} - {self.score}%"
    
    def get_total_questions(self):
        return len(self.user_answers)
    
    def get_correct_count(self):
        correct = 0
        for qid, answer in self.user_answers.items():
            if answer == self.correct_answers.get(qid):
                correct += 1
        return correct
