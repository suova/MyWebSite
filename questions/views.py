import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from questions.forms import *
from .pagination import *
from .models import *
from django.contrib import auth, messages


def index(request, page='1'):
    questions = pagination(request, Question.objects.newest(), 4, page)
    title = "New Questions"
    return render(request, 'questions/index.html', {'questions': questions, 'title': title})


def hot(request, page='1'):
    questions_ = pagination(request, Question.objects.hot(), 5, page)
    title = "Top Questions"
    return render(request, 'questions/index.html', {'questions': questions_, 'title': title})


def ask(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(request.user)
            return HttpResponseRedirect(reverse('question', kwargs={'question_id': q.id}))
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})


def question(request, question_id):
    question_ = get_object_or_404(Question, pk=question_id)
    answers = question_.answer_set.all()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                answer = form.save(question_, request.user)
                return HttpResponseRedirect(reverse('question', kwargs={'question_id': question_id}))
        return HttpResponseRedirect('/login')
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


def settings(request, pk):
    obj = get_object_or_404(Profile, username=pk)

    form = AccountSettings(request.POST or None, instance=obj)

    if form.is_valid():
        print(form.cleaned_data.get('avatar'))
        obj = form.save(commit=False)
        print(obj.photo.url)
        obj.save()
        return HttpResponseRedirect('/index')

    else:
        p = {'form': form}
    return render(request, 'register/accountSettings.html', p)


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
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
