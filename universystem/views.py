from audioop import mul
import email
from email import message
from email.mime import image
import errno
import re
import sys, uuid
from urllib.parse import uses_relative
from django.http import Http404, HttpResponse, JsonResponse
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateResponseMixin,View
from requests import request
from django.template.loader import render_to_string
from .forms import UserUpdateForm, ProfileUpdateForm, CreateUserForm, UserRegistrationForm, ProfileForm, LecturesForm, LecturesTextForm, ImageForm
from .models import Answer, Question, Result, Topics, User, Quiz, Chapters, Profile,Lectures,Lectures_text,EnrollCource, Image, Article
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm


class QuizListView(ListView):
    model = Quiz
    template_name = "quiz_main.html"


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quiz.html', {'obj': quiz})

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, pk):
    # print(request.POST)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100/quiz.numbers_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q):{'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q):'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed':True, 'score':score_, 'results':results})
        else:
            return JsonResponse({'passed': False, 'score':score_, 'results':results})

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'Логин табылмады...')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Логин тексерілімнен өткен жоқ! Электронды поштаңызды тексеріңіз...')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(request, 'Қате құпия сөз...')
            return redirect('/login')

        login(request, user)
        return redirect('/topics')



        # user = authenticate(request, username = username, password=password)
        # if user is not None:
        #     login(request, user)
        #     if 'next' in request.POST:
        #         return redirect(request.POST.get('next'))
        #     else:
        #         return redirect('topics')

        # else:
        #     messages.info(request, 'username incorrect')


    context = {}
    return render(request, "registration/login.html", context)

def register(request):

    # if request.POST == 'POST':
    #     form = CustomUserCreationForm()
    #     if form.is_valid():
    #         form.save()
    #         email = form.cleaned_data.get('email')
    #         password = form.cleaned_data.get('password1')
    #         user = authenticate(email=email, password=password)
    #         messages.success(request, 'Account created successfully')
    #         send_mail_after_register(request, user)
    #         return redirect('/register/token')

    # else:
    #     form = CustomUserCreationForm()
    # context = {
    #     'form':form
    # }

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        # password2 = request.POST.get('password2')


    try:

        if User.objects.filter(username = username).first():
            messages.success(request, 'логин бос емес')
            return redirect('/register')

        if User.objects.filter(email = email).first():
            messages.success(request, 'эл.пошта бос емес')
            return redirect('/register')

        user_obj = User.objects.create(username=username, email=email)
        user_obj.set_password(password1)
        user_obj.save()

        auth_token = str(uuid.uuid4())

        profile_obj = Profile.objects.create(user=user_obj, auth_token = auth_token)
        profile_obj.save()

        send_mail_after_register(email, auth_token)

        return redirect('/register/token')

    except Exception as e:
        print(e)


    # form = CreateUserForm()
    # if request.method == "POST":
    #     form = CreateUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         user = form.cleaned_data.get('username')
    #         messages.success(request, 'Сіз тіркелдіңіз' + user)
    #         return redirect('login')
    # else:
    #     form = CreateUserForm()
    # context = {"form": form}

    return render(request, "registration/registration.html")

def success(request):
    return render(request, 'registration/success.html')

def token_send(request):
    return render(request, 'registration/token_send.html')

def error(request):
    return render(request, 'registration/error.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Аккаунт тексеруден өтті!')
                return redirect('/login')


            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Сіздің аккаунт тексеруден бұрын өткен...')
            return redirect('/login')
        else:
            return redirect('/register/error')

    except Exception as e:
        print(e)

# def send_mail_after_register(request, user):
#     context = {
#         'user': user,
#         'token': token_generator.make_token(user),
#         }
#     message = render_to_string(
#         template_name='registration/verify.html',
#         context=context
#     )
#     email = message.EmailMessage(
#         'Verify Email',
#         message,
#         to =[user.email],

#     )
#     email.send()

def send_mail_after_register(email, auth_token):
    subject = 'Аккаунт верификациясы'
    message = f'Верификациядан өту үшін сілтемеге басыңыз https://pythonplatformkz.herokuapp.com/register/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



@login_required(login_url="/login/")
def view_profile(request):
    result = Result.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'result': result
    }
    return render(request, 'ProfileView.html', context)

@login_required(login_url="/login/")
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Аккаунт жаңа баптаулары сақталды')
            return redirect('universystem:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user': request.user,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'editprofile.html', context)

@login_required(login_url="/login/")
def runcode(request):
    return render(request, 'compiler.html')



def homepage(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')


        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email , 'pythonplatformkz@gmail.com']
        contact_message = "%s: %s via %s" % (
            name ,
            message ,
            email)

        if subject:

            send_mail(
                subject,
                contact_message,
                from_email,
                to_email,
                fail_silently=False,
            )


        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('universystem:topics')

        else:
            messages.info(request, 'Қате логин терілді...')


    context = {}


    return render(request, 'index.html',context)






@login_required(login_url="/login/")
def article_list(request, slug):
    # posts = None
    # if slug is not None:
    article = get_object_or_404(Article, slug=slug)

    # search_query = request.GET.get('search', '')
    # if search_query:
    #     article = Article.objects.filter(title__icontains= search_query)
    # else:
    #     article = Article.objects.all()


    context = {
        'article': article,
        'title': article.title,
        'id_selected': article.article_id,
        }
    return render(request, 'chapter.html', context)

@login_required(login_url="/login/")
def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        articles = Article.objects.filter(
            Q(title__icontains=searched) |
            Q(topic1=searched) |
            Q(topic2=searched) |
            Q(topic3=searched) |
            Q(body1__icontains=searched)|
            Q(body2__icontains=searched)|
            Q(body3__icontains=searched)
            )

        return render(request, "search_venues.html", {'searched':searched, 'articles': articles})
    else:
        return render(request, "search_venues.html", {})





@login_required(login_url="/login/")
def topics(request):
    topics = Article.objects.all()
    context = {'topics': topics}
    return render(request, "home.html", context)

def chapters(request):     # form = ChaptersForm()
    # chapters = Chapters.objects.filter(user=request.user)
    chapters = Chapters.objects.all()

    return render(request, "home.html")

def post_detail(request, slug):
    post = Article.objects.get(slug=slug)
    context = {'post': post}

    return render(request, "lesson.html", context)

@login_required(login_url="/login/")
def exam (request):

    return render(request, "exam.html")



