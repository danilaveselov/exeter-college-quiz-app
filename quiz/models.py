from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('quiz:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
