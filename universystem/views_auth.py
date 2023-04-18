import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from platforma import settings
from universystem.models import Profile


def login_View(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'Логин табылмады...')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Логин тексерілімнен өткен жоқ! Электронды поштаңызды тексеріңіз...')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(request, 'Қате құпия сөз...')
            return redirect('/login')

        login(request, user)
        return redirect('/topics')
    return render(request, "registration/login.html")


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=email).exists():
            message = 'Пользователь с таким Email уже существует'
            return render(request, 'registration.html', {'message': message})
        if password == password2:
            try:
                user = User.objects.create_user(username=email, password=password)
                user.first_name = username
                user.save()
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/topics")
            except:
                message = 'Ошибка регистрации'
                return render(request, 'registration.html', {'message': message})
        else:
            message = 'Пароли не совпадают'
            return render(request, 'registration.html', {'message': message})
    else:
        return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/topics')
        else:
            message = 'Неверный логин или пароль'
            return render(request, 'login.html', {'message': message})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')
# def register(request):

#     if request.method == 'POST':
#
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         # password2 = request.POST.get('password2')
#
#
#     try:
#
#         if User.objects.filter(username=username).first():
#             messages.success(request, 'логин бос емес')
#             return redirect('/register')
#
#         if User.objects.filter(email=email).first():
#             messages.success(request, 'эл.пошта бос емес')
#             return redirect('/register')
#
#         user_obj = User.objects.create(username=username, email=email)
#         user_obj.set_password(password1)
#         user_obj.save()
#
#         auth_token = str(uuid.uuid4())
#
#         profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
#         profile_obj.save()
#
#         send_mail_after_register(email, auth_token)
#
#         return redirect('/register/token')
#
#     except Exception as e:
#         print(e)
#
#
#     # form = CreateUserForm()
#     # if request.method == "POST":
#     #     form = CreateUserForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         user = form.cleaned_data.get('username')
#     #         messages.success(request, 'Сіз тіркелдіңіз' + user)
#     #         return redirect('login')
#     # else:
#     #     form = CreateUserForm()
#     # context = {"form": form}
#
#     return render(request, "registration/registration.html")


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
