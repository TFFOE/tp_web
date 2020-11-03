from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
import logging

logger = logging.getLogger(__name__)
q_num = 54
t_num = q_num // 7
a_num = q_num * 4

tags = [
    {
        'id': i,
        'name' : f"tag{i}",
        'priority' : randint(1, 4),
    } for i in range(t_num)
]

answers = [
    {
        'id': i,
        'q_id': randint(0, q_num - 1),
        'text': f"Answer №{i}. "*20,
        'likes_counter': randint(0, 10),
    } for i in range(a_num)
]

questions = [
    {
        'id': idx,
        'title': f'Title №{idx + 1}',
        'text': f'My question text {idx + 1}. ' * 100,
        'likes_counter': randint(50, 200),
        'answers_counter': len([ans for ans in answers if idx == ans['q_id']]),
        'tags': [
            tags[randint(0, t_num//2)],
            tags[randint(t_num//2 + 1, t_num - 1)]
        ]
    } for idx in range(q_num)
]


def index(request):
    page = request.GET.get('page')
    paginator = Paginator(questions, 3)

    try:
        question_page = paginator.page(page)
    except PageNotAnInteger:
        question_page = paginator.page(1)
    except EmptyPage:
        question_page = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'questions': question_page,
    })

def question(request, id):
    curr_answers = [ans for ans in answers if id == ans['q_id']]
    page = request.GET.get('page')
    paginator = Paginator(curr_answers, 3)

    try:
        answers_page = paginator.page(page)
    except PageNotAnInteger:
        answers_page = paginator.page(1)
    except EmptyPage:
        answers_page = paginator.page(paginator.num_pages)

    return render(request, 'question.html', {
        'question': questions[id],
        'answers': answers_page,
        'id': id,
    })

def tag(request, tag):
    tagged = [question 
        for question in questions
        for q_tag in question['tags']
        if tag == q_tag['name']]

    paginator = Paginator(tagged, 3)
    page = request.GET.get('page')

    try:
        tags_page = paginator.page(page)
    except PageNotAnInteger:
        tags_page = paginator.page(1)
    except EmptyPage:
        tags_page = paginator.page(paginator.num_pages)

    return render(request, 'tag.html', {
        'questions': tags_page,
        'tag': tag,
    })

def hot(request):
    return render(request, 'hot.html', {
        'questions': questions[:3:2]
    })

def ask(request):
    return render(request, 'ask.html', {})

def login(request):
    return render(request, 'login.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def right(request):
    return render(request, 'right.html', {
        'tags': tags,
    })