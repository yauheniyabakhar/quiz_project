from django.contrib import admin
from .models import Topic, Quiz, Question, Choice, Result, QuizComment, Profile

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 0

class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'user']
    list_filter = ('title', 'topic', 'user')
    search_fields = ['title', 'topic__name']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text']
    list_filter = ('quiz', )
    search_fields = ['quiz__title', 'text']
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_correct']
    list_filter = ('question', )
    search_fields = ['question__text']

class QuizCommentAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'date_created', 'user', 'content']
    search_fields = ['user__username', 'quiz__title']

class ResultAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'quiz__title']

admin.site.register(Topic)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(QuizComment, QuizCommentAdmin)
admin.site.register(Profile)
