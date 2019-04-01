from django.urls import path

from . import views

urlpatterns = [
    path('', views.questions_list, name='questions_list'),
    path('ask', views.ask_question, name='ask_question'),
    path('question/<question_id>', views.question_question, name='question'),
    path('tag/<tag_name>', views.tag_question, name='tag'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),

]
