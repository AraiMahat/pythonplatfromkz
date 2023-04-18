from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Answer, Question, Result, Quiz, Chapters, Article


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
        multiplier = 100 / quiz.numbers_of_questions
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
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})


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
        to_email = [from_email, 'pythonplatformkz@gmail.com']
        contact_message = "%s: %s via %s" % (
            name,
            message,
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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('universystem:topics')

        else:
            messages.info(request, 'Қате логин терілді...')
    return render(request, 'index.html')


@login_required(login_url="/login/")
def article_list(request, slug):
    article = get_object_or_404(Article, slug=slug)
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
            Q(body1__icontains=searched) |
            Q(body2__icontains=searched) |
            Q(body3__icontains=searched)
        )

        return render(request, "search_venues.html", {'searched': searched, 'articles': articles})
    else:
        return render(request, "search_venues.html", {})


@login_required(login_url="/login/")
def topics(request):
    topic = Article.objects.all()
    context = {'topics': topic}
    return render(request, "topics.html", context)


def chapters(request):
    chapter = Chapters.objects.all()
    return render(request, "topics.html")


def post_detail(request, slug):
    post = Article.objects.get(slug=slug)
    context = {'post': post}
    return render(request, "lesson.html", context)


@login_required(login_url="/login/")
def exam(request):
    return render(request, "exam.html")
