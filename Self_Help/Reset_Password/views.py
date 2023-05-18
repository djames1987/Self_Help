from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from .forms import SecurityQuestions, ChangePassword, LookUpUser, ForgotPassword, ResetPassword
from .models import Post
from .Security_Questions import Security_Questions
from . import context_processors
import subprocess

ms_identity_web = settings.MS_IDENTITY_WEB


def index(request):
    request.session['TempAuth'] = False
    if request.user.is_authenticated():
        return HttpResponseRedirect("home")
    else:
        return render(request, "auth/login")


def login(request):
    request.session['TempAuth'] = False
    if request.identity_context_data.authenticated:
        return HttpResponseRedirect("/home")
    else:
        return render(request, "main/login.html")


@ms_identity_web.login_required
def passwordReset(request):
    if request.method == "POST":
        clamedata = context_processors.context(request)
        form = ChangePassword(request.POST)
        if form.is_valid():

            action = 'new'
            username = clamedata['claims_to_display']['preferred_username']
            oldpass = form.cleaned_data['old_pass']
            newpass = form.cleaned_data['new_pass']
            pass_string = str(action + '\n' + username + '\n' + newpass + '\n' + oldpass)
            process = subprocess.Popen(['python', 'que_test_2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=bytes(pass_string, 'utf-8'))

            return HttpResponseRedirect("/home")

    else:
        form = ChangePassword()
    return render(request, "main/password_reset.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SecurityQuestions(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            clamedata = context_processors.context(request)
            data.onprem_sid = clamedata['claims_to_display']['onprem_sid']
            data.name = clamedata['claims_to_display']['name']
            data.email = clamedata['claims_to_display']['upn']
            data.question_one = form.cleaned_data['question_one']
            data.answer_one = form.cleaned_data['answer_one']
            data.question_two = form.cleaned_data['question_two']
            data.answer_two = form.cleaned_data['answer_two']
            data.question_three = form.cleaned_data['question_three']
            data.answer_three = form.cleaned_data['answer_three']
            data.save()
            return HttpResponseRedirect("/home")
    form = SecurityQuestions()
    return render(request, 'main/register.html', {"form": form})


def lookup_user(request):
    form = LookUpUser(request.POST)
    if form.is_valid():
        email = form['email']
        test = Post.objects.all()
        if test.filter(email=email.data):
            request.session['_email'] = email.data
            return redirect('/forgot_password')
        else:
            messages.info(request, 'Can not find email address.')
            return redirect('/lookup_login')
    return render(request, 'main/lookup_login.html', {"form": form})


def forgot_password(request):
    email = request.session.get('_email')
    data = Post.objects.get(email=email)
    question_one = Security_Questions[int(data.question_one)][1]
    question_two = Security_Questions[int(data.question_two)][1]
    question_three = Security_Questions[int(data.question_three)][1]
    data = Post.objects.get(email=email)
    q1 = False
    q2 = False
    q3 = False

    if request.method == "POST":
        form = ForgotPassword(request.POST)
        if form.is_valid():
            if form.cleaned_data['answer_one'] == data.answer_one:
                q1 = True
            if form.cleaned_data['answer_two'] == data.answer_two:
                q2 = True
            if form.cleaned_data['answer_three'] == data.answer_three:
                q3 = True
            if q1 == True and q2 == True and q3 == True:
                request.session['TempAuth'] = True
                return HttpResponseRedirect("/forgot_password_auth")
    form = ForgotPassword()
    return render(request, 'main/forgot_password.html', {"form": form, "q1": question_one, "q2": question_two, "q3": question_three})


def forgot_password_auth(request):
    if request.session['TempAuth'] == True:
        if request.method == "POST":
            form = ResetPassword(request.POST)
            if form.is_valid():
                action = 'reset'
                username = request.session.get('_email')
                newpass = form.cleaned_data['new_pass']
                pass_string = str(action + '\n' + username + '\n' + newpass)
                process = subprocess.Popen(['python', 'que_test_2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=bytes(pass_string, 'utf-8'))
                request.session['TempAuth'] = False
                return HttpResponseRedirect("/login")

        form = ResetPassword()
        return render(request, "main/forgot_password_auth.html", {"form": form})

    return HttpResponseRedirect("/login")


@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')


@ms_identity_web.login_required
def home(request):
    return render(request, "main/home.html")
