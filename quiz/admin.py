from django.contrib import admin

from .models import (
    Quiz,
    Question,
    Answer
)


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Quiz, QuizAdmin)
