from django.contrib.auth.decorators import login_required
from django.urls import path

from questions.models import LikeDislike, Question, Answer
from . import views


urlpatterns = [
    path('', views.index, name='questions'),
    path('hot_questions', views.hot, name='hot'),
    path('ask', views.ask, name='ask'),
    path('question/<question_id>', views.question, name='question'),
    path('tag/<tag_name>', views.tag_then_questions, name='tag'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('settings/<pk>', views.settings, name='settings'),
    path('question/<question_id>/like',
         login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.LIKE)),
         name='article_like'),
    path('question/<question_id>/dislike',
         login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.DISLIKE)),
         name='article_dislike'),
    path('question/<question_id>/like',
         login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDislike.LIKE)),
         name='comment_like'),
    path('question/<question_id>/dislike',
         login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDislike.DISLIKE)),
         name='comment_dislike'),

]
