from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from questions.forms import *
from .pagination import *
from .models import *
from django.contrib import auth


def index(request, page='1'):
    questions = pagination(request, Question.objects.newest(), 4, page)
    title = "New Questions"
    return render(request, 'questions/index.html', {'questions': questions, 'title': title})


def hot(request, page='1'):
    questions_ = pagination(request, Question.objects.hot(), 5, page)
    title = "Top Questions"
    return render(request, 'questions/index.html', {'questions': questions_, 'title': title})


@login_required
def ask(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(request.user, 0)
            return HttpResponseRedirect(reverse('question', kwargs={'question_id': q.id}))
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})

def accounts(request):
    return render(request, 'questions/accounts.html')




def question(request, question_id):
    question_ = get_object_or_404(Question, pk=question_id)

    answers = question_.answer_set.all()


    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(question_, request.user)
            return HttpResponseRedirect(reverse('question', kwargs={'question_id': question_id}))
    else:
        form = AnswerForm()
    return render(request, 'questions/question.html',
                  {'question': question_, 'answers': answers, 'form': form})


def tag_then_questions(request, tag_name, page=1):
    tag_questions = Question.objects.tag_search(tag_name)
    questions = pagination(request, tag_questions, 2, page)
    return render(request, 'questions/tagThenQuestions.html', {'tag': tag_name, 'questions': questions})


def login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})

@login_required
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)



def settings(request):
    return render(request, 'register/accountSettings.html', {})


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.avatar = form.cleaned_data.get('avatar')
            user.save()
            my_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=my_password)
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            print(form.is_valid())
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'register/signup.html', {'form': form})

# python manage.py runserver source venv/bin/activate
