from rest_framework import serializers

from .models import Quiz,TakenQuiz,Answer,Question,RandomQuiz,Subject,StudentAnswer
from frontend.serializers import ProfileSerializer



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Quiz
        fields = ['id','name','subject']
class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id','text','question']
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ['id','quiz','text','codesample','answers']




class TakenQuizSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    student = ProfileSerializer()
    class Meta:
        model = TakenQuiz
        fields = ['id','quiz','score','date','student']


class RandomQuizSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    student = ProfileSerializer()
    class Meta:
        model = RandomQuiz
        fields = ['id','quiz','student','questions']

class StudentAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentAnswer
        fields = '__all__'

