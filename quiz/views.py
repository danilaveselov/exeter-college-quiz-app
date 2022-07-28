from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.http import Http404
from django.shortcuts import (
    redirect,
    render
)
from django.urls import (
    reverse,
    reverse_lazy
)
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    DeleteView,
    FormMixin,
    UpdateView
)
from django.views.generic.list import ListView

from .forms import (
    AnswerInlineFormset,
    QuestionForm,
    QuizForm
)
from .models import (
    Answer,
    Question,
    Quiz
)


class AuthRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = '/'


class StaffRequiredMixin(AuthRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class SuperUserRequiredMixin(AuthRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class QuizListView(AuthRequiredMixin, ListView):
    model = Quiz


class QuizDetailView(AuthRequiredMixin, DetailView):
    model = Quiz


class QuizCreateView(SuperUserRequiredMixin, CreateView):
    model = Quiz
    fields = ('name', 'description')


class QuizUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Quiz
    fields = ('name', 'description')


class QuizDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz:list')


class QuizStartView(StaffRequiredMixin, FormMixin, DetailView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_start.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'quiz': self.get_object(),
        })
        return kwargs

    def post(self, request, *args, **kwargs):
        form = QuizForm(quiz=self.get_object(), data=request.POST)
        if form.is_valid():
            max_score = 0
            score = 0
            for answer_pk in form.cleaned_data.values():
                answer = Answer.objects.get(pk=answer_pk)
                max_score += 1
                if answer.is_correct:
                    score += 1
            return render(
                request,
                'quiz/results.html',
                {'max_score': max_score, 'score': score, 'quiz': form.quiz}
            )


class QuestionCreateView(SuperUserRequiredMixin, CreateView):
    form_class = QuestionForm
    model = Question

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answer_form = AnswerInlineFormset()

        return self.render_to_response(
            self.get_context_data(form=form, answer_form=answer_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answer_form = AnswerInlineFormset(self.request.POST)

        if form.is_valid() and answer_form.is_valid():
            return self.form_valid(form, answer_form)
        return self.form_invalid(form, answer_form)

    def form_valid(self, form, answer_form):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        self.object = form.save(commit=False)
        self.object.quiz = quiz
        self.object.save()

        answer_form.instance = self.object
        answer_form.save()
        return redirect(reverse('quiz:detail', kwargs={'slug': quiz.slug}))

    def form_invalid(self, form, answer_form):
        return self.render_to_response(
            self.get_context_data(form=form, answer_form=answer_form)
        )

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)

        try:
            context['quiz'] = Quiz.objects.get(slug=self.kwargs['slug'])
        except Quiz.DoesNotExist:
            raise Http404('Quiz does not exist.')

        if self.request.POST:
            context['form'] = QuestionForm(self.request.POST)
            context['answer_form'] = AnswerInlineFormset(self.request.POST)
        else:
            context['form'] = QuestionForm()
            context['answer_form'] = AnswerInlineFormset()

        return context


class QuestionDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Question

    def get_success_url(self):
        quiz_slug = self.object.quiz.slug
        return reverse('quiz:detail', kwargs={'slug': quiz_slug})


class QuestionUpdateView(SuperUserRequiredMixin, UpdateView):
    form_class = QuestionForm
    model = Question

    def get_success_url(self):
        quiz_slug = self.object.quiz.slug
        return reverse('quiz:detail', kwargs={'slug': quiz_slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answer_form = AnswerInlineFormset(
            self.request.POST,
            instance=self.object
        )

        if form.is_valid() and answer_form.is_valid():
            return self.form_valid(form, answer_form)
        return self.form_invalid(form, answer_form)

    def form_valid(self, form, answer_form):
        self.object = form.save(commit=False)
        self.object.save()

        answer_form.instance = self.object
        answer_form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, answer_form):
        return self.render_to_response(
            self.get_context_data(form=form, answer_form=answer_form)
        )

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = QuestionForm(
                self.request.POST,
                instance=self.object
            )
            context['answer_form'] = AnswerInlineFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            context['form'] = QuestionForm(instance=self.get_object())
            context['answer_form'] = AnswerInlineFormset(
                instance=self.get_object()
            )

        return context
