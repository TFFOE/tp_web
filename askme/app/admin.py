from django.contrib import admin
from .models import Question, Tag, Answer, Profile, AnswerLike, QuestionLike

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(AnswerLike)
admin.site.register(QuestionLike)