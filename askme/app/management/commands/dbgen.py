from itertools import islice
from django.core.management.base import BaseCommand, CommandError
from random import randint, choice, choices, getrandbits, sample
from faker import Faker
from app.models import Question, Tag, Answer, User, AnswerLike, QuestionLike, Profile
from django.contrib.auth.models import User
# generation consequence

#===========================================
# MODEL             NUM         RECOMMENDED
#===========================================
# Users (Profiles)  x100        (10 000)
# Tags              x300        (10 000)
# Questions         x1000       (100 000)
# QuestionLikes     x10000      (300 000)
# Answers           x10000      (1 000 000)
# AnswerLikes       x20000      (1 700 000)
#===========================================

faker = Faker('ru_RU')

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--qlikes', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--alikes', type=int)
    
    def handle(self, *args, **options):
        self.num_users = 10
        self.num_tags = 30
        self.num_questions = 100
        self.num_qlikes = 1000
        self.num_answers = 1000
        self.num_alikes = 2000


        if options['users']:
            self.num_users = options['users']
        if options['questions']:
            self.num_questions = options['questions']
        if options['tags']:
            self.num_tags = options['tags']
        if options['answers']:
            self.num_answers = options['answers']
        if options['alikes']:
            self.num_alikes = options['alikes']
        if options['qlikes']:
            self.num_qlikes = options['qlikes']

        # Генерация БД
        
        # for i in range(options['users']):
            #self.stdout.write(self.style.SUCCESS(faker.name()))

        self.generate_users()
        self.generate_tags()
        self.generate_questions()
        self.generate_question_to_tags_link()
        self.generate_question_likes()
        self.generate_answers()
        self.generate_answer_likes()
    
    def generate_answer_likes(self):
        user_ids = list(
            User.objects.values_list('id', flat = True)
        )
        answers = list(
            Answer.objects.values_list('id', flat = True)
        )
        for uid in user_ids:
            liked = sample(answers, randint(min(10, self.num_questions), min(self.num_alikes/self.num_users, self.num_questions)))
            alikes = (AnswerLike(
                value = bool(getrandbits(1)),
                user_id = uid,
                linked_with_id = a_liked
            ) for a_liked in liked)
            AnswerLike.objects.bulk_create(alikes)

    def generate_answers(self):
        user_ids = list(
            User.objects.values_list('id', flat = True)
        )
        questions = list(
            Question.objects.values_list('id', flat = True)
        )
        for uid in user_ids:
            answered = sample(questions, randint(min(10, self.num_questions), min(self.num_answers/self.num_users, self.num_questions)))
            answers = (Answer(
                user_id = uid,
                question_id = q_answered,
                text = faker.text(),
                publication_date = faker.date(),
                right = bool(getrandbits(1))
            ) for q_answered in answered)
            Answer.objects.bulk_create(answers)

    def generate_question_likes(self):
        user_ids = list(
            User.objects.values_list('id', flat = True)
        )
        questions = list(
            Question.objects.values_list('id', flat = True)
        )
        for uid in user_ids:
            liked = sample(questions, randint(min(10, self.num_questions), min(self.num_qlikes/self.num_users, self.num_questions)))
            qlikes = (QuestionLike(
                value = bool(getrandbits(1)),
                user_id = uid,
                linked_with_id = q_liked
            ) for q_liked in liked)
            QuestionLike.objects.bulk_create(qlikes)

    def generate_question_to_tags_link(self):
        tags = list(
            Tag.objects.values_list('id', flat = True)
        )
        for question in Question.objects.all():
            question.tags.set(choices(tags, k = randint(0, min(3, self.num_tags))))

    def generate_tags(self):
        tags = (Tag(
            name = faker.unique.word()
        ) for i in range(self.num_tags))
        Tag.objects.bulk_create(tags)

    def generate_questions(self):
        user_ids = list(
            User.objects.values_list('id', flat = True)
        )
        questions = (Question(
            text = faker.text(),
            publication_date = faker.date(),
            author_id = choice(user_ids),
            title = faker.sentence()[:-1] + '?',
        )
        for i in range(self.num_questions))
    
        Question.objects.bulk_create(questions)

    def generate_users(self):
        user_data = (User(
            username = faker.name(),
            password = faker.password(),
            email = faker.email(),
        ) for i in range(self.num_users))

        User.objects.bulk_create(user_data)

        user_ids = list(
            User.objects.values_list('id', flat=True)
        )

        img_path_options = (
            'media/clipart1717870.png',
            'media/user-avatar.png',
        )

        profile_data = (Profile(
            user_id = uid,
            avatar = choice(img_path_options)
            ) for uid in user_ids)

        Profile.objects.bulk_create(profile_data)