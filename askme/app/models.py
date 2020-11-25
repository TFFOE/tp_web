from django.db import models
from django.contrib.auth.models import User
import operator
from django.conf import settings


class LikeManager(models.Manager):
    # def get_rating(self, instance):
    #     return self.- self.get_dislikes(instance).count()
    pass

class TagManager(models.Manager):
    pass


class ProfileManager(models.Manager):
    def get_rating(self):
        user_questions = self.question_set.all()
        sum_rating = 0
        for q in user_questions:
            sum_like = 0
            for like in QuestionLike.objects.filter(linked_with_id = q.pk):
                if (like.value == True):
                    sum_like += 1
                else:
                    sum_like -= 1
            sum_rating += sum_like

        user_answers = self.answer_set.all()
        for a in user_answers:
            sum_like = 0
            for like in AnswerLike.objects.filter(linked_with_id = a.pk):
                if (like.value == True):
                    sum_like += 1
                else:
                    sum_like -= 1
            sum_rating += sum_like
        return sum_rating


class AnswerManager(models.Manager):
    def get_rating(self):
        votes = self.answerlike_set
        likes = votes.filter(value=True).count()
        dislikes = votes.filter(value=False).count()
        return likes - dislikes


class QuestionManager(models.Manager):
    def get_rating(self):
        votes = self.questionlike_set
        likes = votes.filter(value=True).count()
        dislikes = votes.filter(value=False).count()
        return likes - dislikes

    def hot(self):
        ordered = sorted(
            self.all(), 
            key=lambda elem: elem.rating(), 
            reverse=True
            )[:10]
        return ordered


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=30,
        verbose_name="Название тега"
    )

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=1000,
        verbose_name="Текст ответа"
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор"
    )
    right = models.BooleanField(
        default=False,
        verbose_name="Ответ является правильным"
    )

    rating = AnswerManager.get_rating

    objects = AnswerManager()

    def __str__(self):
        return self.text[0:20]


class Question(models.Model):
    text = models.CharField(
        max_length=1000,
        verbose_name="Текст вопроса"
    )
    publication_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок вопроса"
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name="Теги"
    )

    rating = QuestionManager.get_rating

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Profile(models.Model):
    avatar = models.ImageField(
        verbose_name="Изображение профиля",
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Связанный пользователь"
    )
    objects = ProfileManager()
    get_rating = ProfileManager.get_rating

    def __str__(self):
        return self.user.username


class AnswerLike(models.Model):
    value = models.BooleanField(
        default=True,
        verbose_name="True if like"
    )
    linked_with = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE,
        verbose_name="Отмеченный ответ"
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь"
    )
    objects = LikeManager()

    def __str__(self):
        return f"Лайк №{self.pk}"

    class Meta:
        unique_together = ('linked_with', 'user',)


class QuestionLike(models.Model):
    value = models.BooleanField(
        default=True,
        verbose_name="True if like"
    )
    linked_with = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        verbose_name="Отмеченный вопрос"
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь"
    )
    objects = LikeManager()

    def __str__(self):
        return f"Лайк №{self.pk}"

    class Meta:
        unique_together = ('linked_with', 'user',)
