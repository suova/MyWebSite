
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .models import *
from django import forms

User = get_user_model()

class LoginForm(forms.Form):
    login = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'login-form-control', 'placeholder': 'Enter your Username here', }),
        max_length=30
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'login-form-control', 'placeholder': '*******', }),
        min_length=8
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
        else:
            raise forms.ValidationError('Wrong login or password')


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Это поле обязательно')
    avatar = forms.FileField(
        label='Avatar',
        widget=forms.ClearableFileInput(),
        required=False
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', "avatar",)



class QuestionForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'login-form-control', 'placeholder': 'Enter question title here', }),
        max_length=100
    )
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(
            attrs={'class': 'login-form-control noresize', 'rows': '14', 'placeholder': 'Enter your question here', }),
        max_length=100000
    )
    tags = forms.CharField(
        label='Tags',
        widget=forms.TextInput(attrs={'class': 'login-form-control', 'placeholder': 'Tag1,Tag2,Tag3'}),
        required=False
    )

    def check_tag(self, tag):
        if (' ' in tag) or ('\n' in tag) or ('\t' in tag):
            raise forms.ValidationError('Tags contain spaces')
        if ('/' in tag) or ('\\' in tag) or ('?' in tag):
            raise forms.ValidationError('You can use only this symbols -+_~&@*%$')
        return tag

    def parse_tags(self, tags):
        self._tag_list = tags.split(',', 10)
        # print self._tag_list

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        self.parse_tags(tags)
        for tag in self._tag_list:
            self.check_tag(tag)
        # return self.check_tag(tag)

    def save(self, user, id):
        data = self.cleaned_data
        if id <= 0:
            q = Question.objects.create(title=data.get('title'), text=data.get('text'),
                                        author=user)
        else:
            q = Question.objects.get(pk=id)
            q.title = data.get('title')
            q.text = data.get('text')
        q.tags.clear()

        q.save()

        for tag_text in self._tag_list:
            if tag_text is not None and tag_text != '':
                tag = Tag.objects.get_or_create(text=tag_text)
                q.tags.add(tag[0])
        q.save()
        return q


class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'login-form-control question-page-input-form-text noresize', 'rows': '5',
                                     'placeholder': 'Enter your answer here', })
    )

    def save(self, question, user):
        data = self.cleaned_data
        return question.answer_set.create(text=data.get('text'), author=user)