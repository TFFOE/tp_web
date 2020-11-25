from .models import Question, Answer, AnswerLike, QuestionLike, Profile, Tag
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def top_tags(request):
    tags = Tag.objects.all()
    top_tags = sorted(tags, reverse=True, key = lambda elem: elem.question_set.count())[:10]
    return {
        'top_tags': top_tags
        }

def questions(request):
    return {'questions': Question.objects.all()}

def tags(request):
    return {'tags': Tag.objects.all()}

def profiles(request):
    return {'profiles': Profile.objects.all()}

def top_users(request):
    users = User.objects.all()
    #top_users = sorted(users, reverse=True, key = lambda elem: Profile.objects.get(user_id = elem.pk).get_rating())[:10]
    top_users = users[:10]
    return {'top_users': top_users}