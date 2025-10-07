from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.db import models
from .models import Quiz, Question, UserQuizAttempt, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, QuizForm, QuestionFormSet, get_question_formset
import json

def home(request):
    """Home page view"""
    return render(request, 'quiz_app/home.html')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'quiz_app/register.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'quiz_app/login.html')

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def edit_profile(request):
    """User profile edit view"""
    # Ensure UserProfile exists for the current user
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('edit_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'quiz_app/edit_profile.html', context)

@login_required
def quiz_list(request):
    """Display all available quizzes"""
    quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'quiz_app/quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    if request.method == 'POST':
        user_answers = {}
        correct_answers = {}
        questions_data = {}
        
        question_ids_str = request.POST.get('question_ids', '')
        question_ids = [int(qid) for qid in question_ids_str.split(',') if qid]
        questions = Question.objects.filter(id__in=question_ids, quiz=quiz)
        
        for question in questions:
            qid = str(question.id)
            user_answer = request.POST.get(f'question_{qid}')
            user_answers[qid] = user_answer
            correct_answers[qid] = question.correct_option
            
            questions_data[qid] = {
                'text': question.text,
                'option_a': question.option_a,
                'option_b': question.option_b,
                'option_c': question.option_c,
                'option_d': question.option_d,
                'correct_option': question.correct_option,
                'explanation': question.explanation,
                'user_answer': user_answer,
            }
        
        correct_count = sum(1 for qid, answer in user_answers.items() 
                           if answer == correct_answers.get(qid))
        total_questions = len(user_answers)
        score = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        attempt = UserQuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=round(score, 2),
            user_answers=user_answers,
            correct_answers=correct_answers,
            questions_data=questions_data,
        )
        
        return redirect('quiz_result', attempt_id=attempt.id)
    
    questions = quiz.get_questions()
    question_ids = [str(q.id) for q in questions]
    context = {
        'quiz': quiz,
        'questions': questions,
        'question_ids': ','.join(question_ids),
    }
    return render(request, 'quiz_app/take_quiz.html', context)

@login_required
def quiz_result(request, attempt_id):
    """Display quiz result"""
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id, user=request.user)
    
    questions_review = []
    for qid, question_data in attempt.questions_data.items():
        user_answer = question_data.get('user_answer')
        correct_answer = question_data.get('correct_option')
        is_correct = user_answer == correct_answer
        
        questions_review.append({
            'text': question_data.get('text'),
            'option_a': question_data.get('option_a'),
            'option_b': question_data.get('option_b'),
            'option_c': question_data.get('option_c'),
            'option_d': question_data.get('option_d'),
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': question_data.get('explanation'),
        })
    
    context = {
        'attempt': attempt,
        'questions_review': questions_review,
        'correct_count': attempt.get_correct_count(),
        'total_questions': attempt.get_total_questions(),
    }
    return render(request, 'quiz_app/quiz_result.html', context)

@login_required
def results_history(request):
    """Display user's quiz history"""
    attempts = UserQuizAttempt.objects.filter(user=request.user)
    return render(request, 'quiz_app/results_history.html', {'attempts': attempts})

def is_staff_user(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff_user)
def admin_dashboard(request):
    """Admin dashboard"""
    total_users = User.objects.count()
    total_quizzes = Quiz.objects.count()
    total_attempts = UserQuizAttempt.objects.count()
    recent_attempts = UserQuizAttempt.objects.all()[:10]
    
    context = {
        'total_users': total_users,
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quiz_app/admin/dashboard.html', context)

@user_passes_test(is_staff_user)
def admin_users(request):
    """Admin user management"""
    users = User.objects.all().order_by('-date_joined')
    user_stats = []
    
    for user in users:
        attempts = UserQuizAttempt.objects.filter(user=user)
        user_stats.append({
            'user': user,
            'total_attempts': attempts.count(),
            'avg_score': attempts.aggregate(models.Avg('score'))['score__avg'] or 0,
        })
    
    return render(request, 'quiz_app/admin/users.html', {'user_stats': user_stats})

@user_passes_test(is_staff_user)
def admin_quiz_list(request):
    """Admin quiz management list"""
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz_app/admin/quiz_list.html', {'quizzes': quizzes})

@user_passes_test(is_staff_user)
def admin_create_quiz(request):
    """Admin create quiz"""
    if request.method == 'POST':
        form = QuizForm(request.POST)
        formset = QuestionFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                quiz = form.save(commit=False)
                quiz.created_by = request.user
                quiz.save()
                
                for question_form in formset:
                    if question_form.cleaned_data.get('text'):
                        question = question_form.save(commit=False)
                        question.quiz = quiz
                        question.save()
                
                messages.success(request, f'Quiz "{quiz.name}" created successfully!')
                return redirect('admin_quiz_list')
    else:
        form = QuizForm()
        formset = QuestionFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'quiz_app/admin/create_quiz.html', context)

@user_passes_test(is_staff_user)
def admin_edit_quiz(request, quiz_id):
    """Admin edit quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        formset = QuestionFormSet(request.POST, instance=quiz)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
                messages.success(request, f'Quiz "{quiz.name}" updated successfully!')
                return redirect('admin_quiz_list')
    else:
        form = QuizForm(instance=quiz)
        formset = QuestionFormSet(instance=quiz)
    
    context = {
        'form': form,
        'formset': formset,
        'quiz': quiz,
    }
    return render(request, 'quiz_app/admin/edit_quiz.html', context)

@user_passes_test(is_staff_user)
def admin_results(request):
    """Admin view all results"""
    attempts = UserQuizAttempt.objects.all()
    
    user_filter = request.GET.get('user')
    quiz_filter = request.GET.get('quiz')
    
    if user_filter:
        attempts = attempts.filter(user_id=user_filter)
    if quiz_filter:
        attempts = attempts.filter(quiz_id=quiz_filter)
    
    users = User.objects.all()
    quizzes = Quiz.objects.all()
    
    context = {
        'attempts': attempts,
        'users': users,
        'quizzes': quizzes,
    }
    return render(request, 'quiz_app/admin/results.html', context)

@user_passes_test(is_staff_user)
def admin_view_result(request, attempt_id):
    """Admin view detailed result"""
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id)
    
    questions_review = []
    for qid, question_data in attempt.questions_data.items():
        user_answer = question_data.get('user_answer')
        correct_answer = question_data.get('correct_option')
        is_correct = user_answer == correct_answer
        
        questions_review.append({
            'text': question_data.get('text'),
            'option_a': question_data.get('option_a'),
            'option_b': question_data.get('option_b'),
            'option_c': question_data.get('option_c'),
            'option_d': question_data.get('option_d'),
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': question_data.get('explanation'),
        })
    
    context = {
        'attempt': attempt,
        'questions_review': questions_review,
        'correct_count': attempt.get_correct_count(),
        'total_questions': attempt.get_total_questions(),
    }
    return render(request, 'quiz_app/admin/view_result.html', context)

@user_passes_test(is_staff_user)
def admin_delete_user(request, user_id):
    """Admin delete user"""
    user = get_object_or_404(User, id=user_id)
    
    if user.is_superuser:
        messages.error(request, 'Cannot delete superuser accounts!')
        return redirect('admin_users')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" has been deleted successfully!')
        return redirect('admin_users')
    
    return redirect('admin_users')
