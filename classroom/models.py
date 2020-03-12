from django.contrib.auth.models import User
from django.db import models
from separatedvaluesfield.models import SeparatedValuesField
from accounts.models import Profile

class Subject(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=300,blank=True, null=True)
    syllabus = models.CharField(max_length=1500, null=True, blank=True)
    provider= models.CharField(max_length=1500, null=True, blank=True)

class Quiz(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=250)
    codesample = models.CharField(max_length=500, blank=True, null=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class TakenQuiz(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)


class RandomQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tempquiz')
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tempanswers')
    questions =models.CharField(max_length=900, null=True, blank=True)
