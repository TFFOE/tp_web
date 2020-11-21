from itertools import islice
from django.core.management.base import BaseCommand, CommandError
from random import randint, choice
from faker import Faker
from app.models import Question, Tag, Answer, User, AnswerLike, QuestionLike

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

num_users = 100
num_tags = 300
num_questions = 1000
num_qlikes = 10000
num_answers = 10000
num_alikes = 20000

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--qlikes', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--alikes', type=int)
    
    def handle(self, *args, **options):
        if options['users']:
            num_users = options['users']
        if options['questions']:
            num_questions = options['questions']
        if options['tags']:
            num_tags = options['tags']
        if options['answers']:
            num_answers = options['answers']
        if options['alikes']:
            num_alikes = options['alikes']
        if options['qlikes']:
            num_qlikes = options['qlikes']

        # Генерация БД
        faker = Faker('ru_RU')
        for i in range(options['users']):
            self.stdout.write(self.style.SUCCESS(faker.name()))