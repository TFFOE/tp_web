from .models import Question, Answer, AnswerLike, QuestionLike, Profile, Tag
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def top_tags(request):
    return {'top_tags': Tag.objects.all()}

def questions(request):
    return {'questions': Question.objects.all()}

def tags(request):
    return {'tags': Tag.objects.all()}

def profiles(request):
    return {'profiles': Profile.objects.all()}

def top_users(request):
    return {'top_users': User.objects.all()}