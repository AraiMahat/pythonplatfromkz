from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required 
app_name = 'universystem'

urlpatterns =[
	path('', views.homepage, name="home"),
	path('register/',views.register,name='register'),
	path('register/success',views.success,name='success'),
	path('register/token',views.token_send,name='token_send'),
	path('register/verify/<auth_token>',views.verify,name='verify'),
	path('register/error',views.error,name='error'),
	# path('login/',auth_views.LoginView.as_view(),name='login'),
	path('login/',views.loginView,name='login'),
	path('logout/',auth_views.LogoutView.as_view(),name='logout'),
	path('profile/',views.view_profile, name='profile'),
	path('topics/',views.topics, name='topics'),
	path('article/<slug:slug>/', views.article_list, name='article'),
	path('lesson/<slug:slug>/', views.post_detail, name='post_detail'),
	path('runcode/', views.runcode, name="runcode"),
	path('search/', views.search_venues, name="search"),
	path('quiz/', login_required(views.QuizListView.as_view()), name="main-quiz"),
	path('quiz/<int:pk>/', views.quiz_view, name="quiz-view"),
	path('quiz/<int:pk>/save/', views.save_quiz_view, name="save-view"),
	path('quiz/<int:pk>/data/', views.quiz_data_view, name="quiz-data-view"),
	path('quiz/exam', views.exam, name="exam"),

	path('profile/edit', views.edit_profile, name="edit_profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)