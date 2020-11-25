from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer, Profile, QuestionLike, AnswerLike, Tag
import logging
from django.contrib import auth
from app.forms import LoginForm

logger = logging.getLogger(__name__)

def index(request):
    page = request.GET.get('page')

    questions = Question.objects.all()
    paginator = Paginator(questions, 3)

    try:
        question_page = paginator.page(page)
    except PageNotAnInteger:
        question_page = paginator.page(1)
    except EmptyPage:
        question_page = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {
        'questions': question_page,
        'answers_count': Question.objects.all()

    })

def question(request, id):
    question = Question.objects.select_related('author').get(pk = id)
    answers = sorted(
        question.answer_set.all(), 
        key=lambda ans: ans.rating(), 
        reverse=True
        )
    page = request.GET.get('page')
    paginator = Paginator(answers, 3)

    try:
        answers_page = paginator.page(page)
    except PageNotAnInteger:
        answers_page = paginator.page(1)
    except EmptyPage:
        answers_page = paginator.page(paginator.num_pages)

    return render(request, 'question.html', {
        'question': question,
        'answers': answers_page,
    })

def tag(request, tag):
    tagged = Tag.objects.get(name = tag).question_set.all()
    
    paginator = Paginator(tagged, 3)
    page = request.GET.get('page')

    try:
        tags_page = paginator.page(page)
    except PageNotAnInteger:
        tags_page = paginator.page(1)
    except EmptyPage:
        tags_page = paginator.page(paginator.num_pages)

    return render(request, 'tag.html', {
        'tagged_questions': tags_page,
        'tag': tag,
    })

def hot(request):
    hot_questions = Question.objects.hot()

    paginator = Paginator(hot_questions, 3)
    page = request.GET.get('page')

    try:
        hot_page = paginator.page(page)
    except PageNotAnInteger:
        hot_page = paginator.page(1)
    except EmptyPage:
        hot_page = paginator.page(paginator.num_pages)


    return render(request, 'hot.html', {
        'hot_questions': hot_page,
    })

def ask(request):
    return render(request, 'ask.html', {})

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        logger.error("REQUEST IS GET")
    elif request.method == 'POST':
        logger.error("REQUEST IS POST")
        form = LoginForm()
        
        user = auth.authenticate(request, username = request.POST.get('login'), password = request.POST.get('password'))
        if user is not None:
            logger.error("IM HERE")
            auth.login(request, user)
            return redirect("/") # Настроить правильный редирект
        else:
            logger.error("IM NOT HERE")

    ctx = {'form': form}
    return render(request, 'login.html', ctx)

def logout(request):
    auth.logout(request)
    return redirect("/")

def settings(request):
    return render(request, 'settings.html', {})

def signup(request):
    return render(request, 'signup.html', {})