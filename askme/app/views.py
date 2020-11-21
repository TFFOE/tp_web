from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
from .models import *
from operator import attrgetter
import logging

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
    curr_question = Question.objects.get(pk = id)
    curr_answers = sorted(
        Answer.objects.get_answers_by_question_pk(id), 
        key=lambda elem: elem.likes_count(), 
        reverse=True
        )
    page = request.GET.get('page')
    paginator = Paginator(curr_answers, 3)

    try:
        answers_page = paginator.page(page)
    except PageNotAnInteger:
        answers_page = paginator.page(1)
    except EmptyPage:
        answers_page = paginator.page(paginator.num_pages)

    return render(request, 'question.html', {
        'question': curr_question,
        'answers': answers_page,
    })

def tag(request, tag):
    tagged = Question.objects.filter(tags__name = tag)
    
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
    return render(request, 'login.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def signup(request):
    return render(request, 'signup.html', {})