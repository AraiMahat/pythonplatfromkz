from django.contrib import admin
from .models import Answer, Profile, Article, Question, Quiz, Result, Topics


admin.site.register(Profile)
admin.site.register(Result)
admin.site.register(Quiz)


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)


class PostAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'title', 'image')
    list_display_links = ('article_id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, PostAdmin)
