from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post
from django.core.paginator import Paginator

# Create your views here.
userGirl = ({'photo': 'images/devochka-color.jpg'})
userBoy = ({'photo': 'images/malchik-color.jpg'})
tags = []

tags.append({'text': "C++"})
tags.append({'text': "Java"})

tags1 = []
tags1.append({'text': "Golang"})
tags1.append({'text': "Python"})
questions = []
for i in range(1, 10):
    questions.append({
        'id': i,
        'title': "Can PowerShell script out SQL Server Reporting Services RDL files? " + str(i),
        'content': "Is it possible to use PowerShell to script out SQL Server Reporting Services rdl files in SQL Server 2008? If so, can someone provide a code example of doing this? This would be a useful replacement for using a 3rd party tool to script out RDL files created by business users outside of my Business Intelligence department. " + str(
            i),
        'tags': tags1,
        'author': userGirl
    })
for i in range(1, 10):
    questions.append({
        'id': i,
        'title': "Debugging report error on SSRS " + str(i),
        'content': "we have a bunch of reports (RDL) on SSRS built using officewriter. Sometimes errors occur in a report after updating the excel template. While the report renders fine, an error occurs on the server when trying to save the report using 'export to excel format for office writer' option. How do we debug to find the cause of the error? " + str(
            i),
        'tags': tags,
        'author': userBoy
    })


def questions_list(request):
    contact_list = questions
    current_page = Paginator(contact_list, 4)
    page = request.GET.get('page')
    contacts = current_page.get_page(page)
    return render(request, 'questions/index.html', {'questions': contacts})


def ask_question(request):
    return render(request, 'questions/ask.html', {})


def question_question(request, question_id):
    return render(request, 'questions/question.html', {'id': question_id, 'question': questions[int(question_id)]})


def tag_question(request, tag_name):
    if (tag_name):
        tag = ({'text': tag_name})

        contact_list = questions
        current_page = Paginator(contact_list, 4)
        page = request.GET.get('page')
        contacts = current_page.get_page(page)
    return render(request, 'questions/tagThenQuestions.html', {'tag': tag, 'questions': contacts})


def login(request):
    return render(request, 'register/login.html', {})


def settings(request):
    return render(request, 'register/accountSettings.html', {})


def register(request):
    return render(request, 'register/signup.html', {})
# p = []
#    for i in range(len(questions)):
 #       if questions['tags'][i] == tag['text']:
  #          p.insert(questions[i])
#python manage.py runserver