
import os
import random

from ckeditor.fields import RichTextField
from django.conf import settings
# from tinymce import HTMLField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    numbers_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="vremya testa")
    required_score_to_pass = models.IntegerField(help_text="required score to pass")

    def __str__(self):
        return f"{self.name} - {self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.numbers_of_questions]

    class Meta:
        verbose_name = 'Тесты'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

    class Meta:
        verbose_name = 'Вопросы'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.user.pk)

    class Meta:
        verbose_name = 'Результаты'
        verbose_name_plural = 'Результаты'


def user_directory_path(instance, filename):
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name


class Profile(models.Model):
    photo = models.ImageField(upload_to='images/profile', null=True, default='img/pfp.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Lectures(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200, null=True, blank=True)
    code = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Лекции'
        verbose_name_plural = 'Лекции'


class LecturesText(models.Model):
    lectures_id = models.ForeignKey(Lectures, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    photo = models.URLField(max_length=200)
    lectures_cod = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class EnrollCourse(models.Model):
    lectures = models.ForeignKey(Lectures, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Article(models.Model):
    article_id = models.ForeignKey(Lectures, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img')
    photo = models.URLField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    topic1 = models.TextField(blank=True)
    topic2 = models.TextField(blank=True)
    topic3 = models.TextField(blank=True)
    body1 = RichTextField(blank=True, null=True)
    body2 = RichTextField(blank=True, null=True)
    body3 = RichTextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    code = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Темы'
        verbose_name_plural = 'Темы'


class Topics(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    image = models.ImageField(upload_to='img')
    topic1 = models.TextField()
    topic2 = models.TextField()
    topic3 = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url_1(self):
        return reverse('topics', args=[str(self.id)])

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Chapters(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Chapters"
        verbose_name_plural = "Chapters"
