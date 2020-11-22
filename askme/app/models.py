from django.db import models
from django.contrib.auth.models import User
import operator
from django.conf import settings


class LikeManager(models.Manager):
    def get_likes(self, instance):
        return self.filter(value=True, linked_with__pk=instance.pk)

    def get_dislikes(self, instance):
        return self.filter(value=False, linked_with__pk=instance.pk)

    def get_rating(self, instance):
        return self.get_likes(instance).count() - self.get_dislikes(instance).count()

    def check_if_liked(self, instance):
        return self.get_likes(instance).count() > 0

    def check_if_disliked(self, instance):
        return self.get_dislikes(instance).count() > 0

    # def press_like(self, user, instance):
    #     defaults = {
    #         'linked_with': self,
    #         'user': user,
    #     }
    #     instance.objects.update_or_create(
    #         defaults, defaults
    #     )


class TagManager(models.Manager):
    def popular_tags(self):
        return self.all()[:10]

    # должен возвращать теги вопроса
    def question_tags(self, question_pk):
        self.filter(question__id=question_pk)
        pass


class ProfileManager(models.Manager):
    def getByUsername(self, username):
        return self.all().filter()

    def get_rating(self):
        user_questions = Question.objects.filter(author_id = self.pk)
        sum_rating = 0
        for q in user_questions:
            sum_like = 0
            for like in QuestionLike.objects.filter(linked_with_id = q.pk):
                if (like.value == True):
                    sum_like += 1
                else:
                    sum_like -= 1
            sum_rating += sum_like

        user_answers = Answer.objects.filter(user_id = self.pk)
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
    def get_all(self):
        return self.all()

    def get_answers_by_question_pk(self, pk):
        return self.filter(question__pk=pk)

    def question_answers_count(self, pk):
        return self.get_answers_by_question_pk(pk).count()

    def get_likes(self):
        return AnswerLike.objects.get_rating(self)

    def user_image(self):
        return Profile.objects.get(user_id = self.author.pk).avatar.url
    # def press_like(self, user):
    #     return LikeManager.press_like(user, self)


class QuestionManager(models.Manager):
    def popular_questions(self):
        return self.all()[:10]

    def answers_count(self):
        return Answer.objects.question_answers_count(self.pk)

    def answers(self):
        return Answer.objects.get_answers_by_question_pk(self.pk)

    def with_special_tag(self, tag):
        import logging
        logger = logging.getLogger(__name__)
        logger.error(tag)
        return self.filter(tag__contains=tag)

    def get_likes(self):
        return QuestionLike.objects.get_rating(self)

    def hot(self):
        unordered = self.all()
        ordered = sorted(unordered, key=lambda elem: elem.likes_count(), reverse=True)[:10]
        return ordered

    def get_username(self):
        return self.user.username

    def user_image(self):
        return Profile.objects.get(user_id = self.author.pk).avatar.url


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
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор"
    )
    right = models.BooleanField(
        default=False,
        verbose_name="Ответ является правильным"
    )
    objects = AnswerManager()
    likes_count = AnswerManager.get_likes
    user_image = AnswerManager.user_image


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

    objects = QuestionManager()
    answers = QuestionManager.answers
    answers_count = QuestionManager.answers_count
    with_special_tag = QuestionManager.with_special_tag
    likes_count = QuestionManager.get_likes
    hot = QuestionManager.hot
    user_image = QuestionManager.user_image

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
