from django import forms
from django.forms import inlineformset_factory

from .models import (
    Answer,
    Question
)


class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = quiz
        for question in self.quiz.question_set.all():
            field_name = "question_%d" % question.pk
            choices = []
            for answer in question.answer_set.all():
                choices.append((answer.pk, answer.answer,))
            self.fields[field_name] = forms.ChoiceField(
                label=question.question,
                required=True, choices=choices,
                widget=forms.RadioSelect
            )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer', 'is_correct')


AnswerInlineFormset = inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    extra=5,
    max_num=5
)
