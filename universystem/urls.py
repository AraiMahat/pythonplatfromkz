from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static 
app_name = 'universystem'

urlpatterns =[
	path('', views.homepage, name="home"),
	path('register/',views.register,name='register'),
	path('login/',auth_views.LoginView.as_view(),name='login'),
	path('logout/',auth_views.LogoutView.as_view(),name='logout'),
	path('profile/',views.view_profile, name='profile'),
	path('topics/',views.topics, name='topics'),
	path('article/<slug:slug>/', views.article_list, name='article'),
	path('lesson/<slug:slug>/', views.post_detail, name='post_detail'),
	path('runcode/', views.runcode, name="runcode"),
	path('search/', views.search_venues, name="search"),
	path('quiz/', views.QuizListView.as_view(), name="main-quiz"),
	path('quiz/<int:pk>/', views.quiz_view, name="quiz-view"),
	path('quiz/<int:pk>/save/', views.save_quiz_view, name="save-view"),
	path('quiz/<int:pk>/data/', views.quiz_data_view, name="quiz-data-view"),
	path('profile/edit', views.edit_profile, name="edit_profile"),



	
	

	path('user/registration', views.UserRegistrationView.as_view(), name='user_registration_page'),
	path('lessons/<int:id>',views.LessonsDetailView.as_view(), name='LessonsDetailView'),
	path('addEroll/<int:id>',views.AddEnrlcourseView.as_view(), name='AddEnrlcourseView'),
	path('add/',views.AddIndexView.as_view(), name='AddIndexView'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)