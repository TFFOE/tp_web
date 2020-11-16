from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class Question(models.Model):
    question_text = models.CharField(
        max_length=1000, verbose_name="Текст вопроса")
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name="Автор")
    title = models.CharField(max_length=100, verbose_name="Заголовок вопроса")
    tags = TaggableManager(blank=True, verbose_name="Теги")


class Tag(models.Model):
    name = models.SlugField(verbose_name="Название тега", unique=True)
    question = models.ManyToManyField(Question, verbose_name="Вопрос")


# class AnswerLike(models.Model):
#     answer
#     user


# class QuestionLike(models.Model):
#     question
#     user


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(
        max_length=1000, verbose_name="Текст ответа")
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL, verbose_name="Автор")


# additional user info
class Profile(models.Model):
    avatar = models.ImageField(verbose_name="Изображение профиля")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Связанный пользователь")
