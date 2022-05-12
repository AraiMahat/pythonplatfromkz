from django.contrib import admin
from .models import Answer, Profile,Lectures,Lectures_text,EnrollCource, Chapters, Image, Article, Question, Quiz, Result, Topics


admin.site.register(Profile)
admin.site.register(Lectures)
admin.site.register(Lectures_text)
admin.site.register(EnrollCource)
admin.site.register(Image)
admin.site.register(Chapters)

admin.site.register(Result)
admin.site.register(Quiz)


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)


admin.site.register(Topics)

class PostAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'title', 'image')
    list_display_links = ('article_id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, PostAdmin)
