from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Option, Result



@login_required
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'home.html', {'quizzes': quizzes})



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'signup.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def start_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        print(request.POST)
        score = 0

        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}', None)
            print("Q:", question.id, "Selected:", selected_option_id)

            if selected_option_id:
                option = Option.objects.filter(
                    id=int(selected_option_id),
                    question=question
                ).first()
                print("Option:", option, "Correct:", option.is_correct if option else None)

                if option and option.is_correct:
                    score += 1

        Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score
        )

        return render(request, 'result.html', {
            'quiz': quiz,
            'score': score,
            'total': questions.count()
        })


    return render(request, 'quiz.html', {
        'quiz': quiz,
        'questions': questions
    })