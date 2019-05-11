from django.urls import path

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
    path('settings', views.settings, name='settings'),
    path('accounts/login/', views.accounts, name='accounts'),

]
