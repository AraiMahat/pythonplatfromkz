from audioop import mul
from email.mime import image
import errno
import re
import sys
from django.http import Http404, JsonResponse
from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateResponseMixin,View
from requests import request
from .forms import UserUpdateForm, ProfileUpdateForm, CreateUserForm, UserRegistrationForm, ProfileForm, LecturesForm, LecturesTextForm, ImageForm
from .models import Answer, Question, Result, Topics, User, Quiz, Chapters, Profile,Lectures,Lectures_text,EnrollCource, Image, Article
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView

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

def view_profile(request):
    result = Result.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'result': result
    }
    return render(request, 'ProfileView.html', context)

def edit_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'editprofile.html', context)

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

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Сіз тіркелдіңіз' + user)
            return redirect('login')
    else:
        form = CreateUserForm()
    
    return render(request, "registration/registration.html", {"form": form})

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('topics')
            
        else:
            messages.info(request, 'username incorrect')


    context = {}
    return render(request, "registration/login.html", context)

class UserRegistrationView(TemplateResponseMixin, View):
    template_name = 'registration/registration.html'

    def get(self,request):
        registration_form = UserRegistrationForm()
        profile_form = ProfileForm()
        return self.render_to_response({'registration_form': registration_form, 'profile_form': profile_form})

    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, files=request.FILES)
        if registration_form.is_valid() and profile_form.is_valid():
            new_user = registration_form.save(commit=False)
        # Set the chosen password
            new_user.set_password(
            registration_form.cleaned_data['password'])
        # Save the User object
            new_user.save()
            profile = profile_form.save(commit = False)
            profile.user = new_user
            profile.save()
            return redirect('universystem:login')
        return self.render_to_response({'registration_form': registration_form, 'profile_form': profile_form})

# class ProfileView(TemplateResponseMixin,View):
#     template_name = 'ProfileView.html'
#     def get(self,request):
#         lectures = Lectures.objects.all()
#         if Profile.objects.filter(user= request.user).exists():
#             lesson = EnrollCource.objects.filter(user= request.user)
#             profile = Profile.objects.get(user = request.user)
#         return self.render_to_response({'profile': profile, 'lectures': lectures, 'lesson': lesson})
#     def profile(request):
#         u_form = UserUpdateForm()
#         p_form = ProfileUpdateForm()
        
#         context = {'u_form': u_form, 'p_form': p_form}
#         return render(request, 'ProfileView.html', context)  


class StudentProfileIndexView(TemplateResponseMixin,View):
    template_name = 'home.html'    #set up pagination
    def get(self, request):
       lectures = Lectures.objects.all()
       return self.render_to_response({'lectures': lectures})

class LessonsDetailView(TemplateResponseMixin,View):
    template_name = 'detail.html'
    def get(self,request, id):
        lectures = Lectures.objects.all()
        lecturesone = Lectures.objects.get(id=id)
        lectures_text = Lectures_text.objects.filter(lectures_id=id)

        return self.render_to_response({'lectures': lectures, 'lecturesone':lecturesone,
         'lectures_text':lectures_text, })

    def post(self,request, id):
        lectures = Lectures.objects.all()
        lecturesone = Lectures.objects.get(id=id)
        lectures_text = Lectures_text.objects.filter(lectures_id=id)
        
        if request.method == "POST":
            codeareadata = request.POST['codearea']

            try:

                original_stdout = sys.stdout
                sys.stdout = open('file.txt', 'w') 

                exec(codeareadata)  

                sys.stdout.close()

                sys.stdout = original_stdout 


                output = open('file.txt', 'r').read()

            except Exception as e:
                sys.stdout = original_stdout
                output = e
                
        return self.render_to_response({'lectures': lectures, 'lecturesone':lecturesone, 
         'lectures_text':lectures_text,'code': codeareadata , 'output': output})

class AddEnrlcourseView(View):

    def post(self,request,id):
        courses_obj = EnrollCource(lectures_id=request.POST['lessonid'], user =request.user)
        courses_obj.save()
        return redirect('universystem:LessonsDetailView',id)

class AddIndexView(TemplateResponseMixin,View):
    template_name = 'test.html'
    def get(self,request):
        lectures_form = LecturesForm()
        lectures = Lectures.objects.all()
        return self.render_to_response({'lectures_form':lectures_form,'lectures':lectures})

    def post(self,request):
        lectures_form = LecturesForm(data=request.POST)
        if lectures_form.is_valid():#тексеру
            lectures_formadd = lectures_form.save(commit=False)
            lectures_formadd.save()
            return redirect('universystem:AddIndexView')
        return self.render_to_response({'lectures_form': lectures_form})

# class AddTextIndexView(TemplateResponseMixin,View):
#     template_name = 'addtext.html'
#     def get(self,request):
#         lectures_text = LecturesTextForm()
#         lectures = Lectures_text.objects.all()
#         return self.render_to_response({'lectures_text':lectures_text,'lectures':lectures})

#     def post(self,request):
#         lectures_text = LecturesTextForm(data=request.POST)
#         if lectures_text.is_valid():#тексеру
#             lectures_formadd = lectures_text.save(commit=False)
#             lectures_formadd.save()
#             return redirect('universystem:AddTextIndexView')
#         return self.render_to_response({'lectures_text': lectures_text,'lectures':lectures})


# def runcode(request):

#     if request.method == "POST":
#         codeareadata = request.POST['codearea']

#         try:
#             #save original standart output reference

#             original_stdout = sys.stdout
#             sys.stdout = open('file.txt', 'w') #change the standard output to the file we created

#             #execute code

#             exec(codeareadata)  #example =>   print("hello world")

#             sys.stdout.close()

#             sys.stdout = original_stdout  #reset the standard output to its original value

#             # finally read output from file and save in output variable

#             output = open('file.txt', 'r').read()

#         except Exception as e:
#             # to return error in the code
#             sys.stdout = original_stdout
#             output = e


#     #finally return and render index page and send codedata and output to show on page

#     return render(request , 'compiler.html', {"code":codeareadata , "output":output})
    

# def runcode(request):
#     if request.method == 'POST':
#         code_part = request.POST['code_area']
#         input_part = request.POST['input_area']
#         y = input_part
#         input_part = input_part.replace("\n"," ").split(" ")
#         def input():
#             a = input_part[0]
#             del input_part[0]
#             return a
#         try:
#             orig_stdout = sys.stdout
#             sys.stdout = open('file.txt', 'w')
#             exec(code_part)
#             sys.stdout.close()
#             sys.stdout=orig_stdout
#             output = open('file.txt', 'r').read()
#         except Exception as e:
#             sys.stdout.close()
#             sys.stdout=orig_stdout
#             output = e
#         print(output)
#     res = render(request,'compiler.html',{"code":code_part,"input":y,"output":output})
#     return res

def runcode(request):
    return render(request, 'compiler.html')



def homepage(request):
    return render(request, 'index.html')


def quiz(request):
    return render(request, 'quiz.html')


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})

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



# def get_queryset(query=None):
#     queryset = []
#     queries = query.split(" ")
#     for q in queries:
#         posts = Article.objects.filter(
#             Q(topic1__icontains=q) |
#             Q(body1__icontains=q)
#         ).distinct()

#         for post in posts:
#             queryset.append(post)
        
#     return list(set(queryset))


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



