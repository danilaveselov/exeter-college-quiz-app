from django.test import TestCase
from quiz.models import (
    Quiz,
    Question,
    Answer
)


class QuizTestCase(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='quiz', description='description')
        self.question = Question.objects.create(
            question='question',
            quiz=self.quiz
        )
        self.answer = Answer.objects.create(
            answer='answer',
            is_correct=True,
            question=self.question
        )

    def test_quiz_model(self):
        self.assertEqual(self.quiz.name, 'quiz')
        self.assertEqual(self.quiz.description, 'description')

    def test_question_model(self):
        self.assertEqual(self.question.question, 'question')
        self.assertEqual(self.question.quiz, self.quiz)

    def test_answer_model(self):
        self.assertEqual(self.answer.answer, 'answer')
        self.assertTrue(self.answer.is_correct)
        self.assertEqual(self.answer.question, self.question)
