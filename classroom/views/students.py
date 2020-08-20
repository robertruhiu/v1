from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.db.models import Q
from django.urls import reverse
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from ..decorators import student_required
from ..forms import TakeQuizForm
from ..models import Quiz, TakenQuiz, User,StudentAnswer,Answer,Subject,RandomQuiz,Question
import random
from transactions.models import OpenCall
from rest_framework import generics
from ..serializers import QuizSerializer,TakenQuizSerializer,RandomQuizSerializer,QuestionSerializer,StudentAnswerSerializer,SubjectSerializer
from accounts.models import Profile
from rest_framework.permissions import IsAuthenticated
class AllQuizzes(generics.ListAPIView):

    serializer_class = QuizSerializer
    def get_queryset(self):


        return Quiz.objects.all() \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)

class TakenQuizzes(generics.ListAPIView):
    serializer_class = TakenQuizSerializer
    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        user = Profile.objects.get(pk=candidate_id)
        return TakenQuiz.objects.filter(user=user)

class QuizQuestions(generics.ListAPIView):
    serializer_class = QuestionSerializer
    def get_queryset(self):
        quiz_id = self.kwargs['quiz']
        return Question.objects.filter(quiz_id=quiz_id)

class TakeQuiz(generics.ListAPIView):
    serializer_class = RandomQuizSerializer
    def get_queryset(self):

        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']

        quiz = get_object_or_404(Quiz, pk=quiz_id)
        student = Profile.objects.get(id=candidate_id)


        questionlist = []
        quizzes = RandomQuiz.objects.filter(student_id=student.id).filter(quiz_id=quiz_id)
        if len(quizzes) >0:
            return quizzes
        else:
            currentquiz = Question.objects.filter(quiz_id=quiz_id)
            for onequestion in currentquiz:
                questionlist.append(onequestion.id)

            questionrandomlist = random.sample(questionlist, 30)
            questions= ','.join(map(str, questionrandomlist))


            obj = RandomQuiz(quiz=quiz, student=student, questions=questions)
            obj.save()
            return RandomQuiz.objects.filter(student_id=student.id).filter(quiz_id=quiz_id)

class PostAnswer(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

class Subjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class UpdateRandomquiz(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = RandomQuiz.objects.all()
    serializer_class = RandomQuizSerializer

class CalculateScore(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenQuizSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']
        student = Profile.objects.get(id=candidate_id)
        quiz = Quiz.objects.get(id=quiz_id)

        correctanswercounter = StudentAnswer.objects.filter(quiz=quiz, student=student, answer__is_correct=True).count()
        score = (correctanswercounter / 30) * 100
        TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
        return TakenQuiz.objects.filter(student=student)

class Taken(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenQuizSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        student = Profile.objects.get(id=candidate_id)
        return TakenQuiz.objects.filter(student=student)

class DeleteQuizAnswer(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentAnswerSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']
        StudentAnswer.objects.filter(quiz_id=quiz_id, student_id=candidate_id).delete()

        return StudentAnswer.objects.filter(student_id=candidate_id)


class DeleteQuizTaken(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenQuizSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']
        TakenQuiz.objects.filter(quiz_id=quiz_id,student_id=candidate_id).delete()

        return TakenQuiz.objects.filter(student_id=candidate_id)
class DeleteQuizRandom(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RandomQuizSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']
        RandomQuiz.objects.filter(quiz_id=quiz_id,student_id=candidate_id).delete()

        return RandomQuiz.objects.filter(student_id=candidate_id)



@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):

    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        queryset = Quiz.objects.all() \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()

        return context



@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset




@login_required
def take(request, pk):
    global tempquiz
    quiz = get_object_or_404(Quiz, pk=pk)

    student = Profile.objects.get(id=request.user.id)
    takenquizlist = []
    quizzes = TakenQuiz.objects.filter(student_id=student.id)
    for onequiz in quizzes:
        takenquizlist.append(onequiz.quiz.name)

    if quiz.name in takenquizlist:
        return redirect('students:taken_quiz_list')
    else:
        questionlist = []
        try:
            tempquiz = RandomQuiz.objects.get(student_id=student.id,quiz_id=pk)


        except RandomQuiz.DoesNotExist:
            currentquiz =Question.objects.filter(quiz_id=pk)
            for onequestion in currentquiz:

                questionlist.append(onequestion.id)
            try:
                questionrandomlist = random.sample(questionlist, 30)
                obj = RandomQuiz(quiz=quiz, student=student, questions=questionrandomlist)
                obj.save()

                return redirect('students:take', pk)
            except:
                pass

        if not tempquiz.questions == None:
            tempquizquestionsids =tempquiz.questions
            randomquestionlist =[]
            for tempquizquestionsid in tempquizquestionsids:
                randomquestionlist.append(int(tempquizquestionsid))
            questions =Question.objects.filter(id__in=randomquestionlist)
            total_questions = len(randomquestionlist)
            total_unanswered_questions = questions.count()
            progress = 100 - round(((total_unanswered_questions - 1) / 30) * 100)
            question = questions.first()
            updatedrandomquestionlist =[]
            updatedrandomquestionlist.append(question.id)

            unanswered_questions = list(set(randomquestionlist) ^ set(updatedrandomquestionlist))

            if request.method == 'POST':
                form = TakeQuizForm(question=question, data=request.POST)
                if form.is_valid():
                    with transaction.atomic():
                        if 'answer' in request.POST:
                            student_answer = form.save(commit=False)
                            student_answer.student = student
                            student_answer.quiz = quiz
                            student_answer.save()
                            randomquizinstance = RandomQuiz.objects.get(quiz_id=pk,student_id=student.id)
                            randomquizinstance.questions = unanswered_questions
                            randomquizinstance.save()

                        else:
                            default_answer = StudentAnswer(quiz=quiz,student=student,answer=Answer.objects.filter(question_id = question.id).last())
                            #TO DO add a conditional to ensure only wrong option is choosen when no answer provided
                            default_answer.save()
                            randomquizinstance = RandomQuiz.objects.get(quiz_id=pk,student_id=student.id)
                            randomquizinstance.questions = unanswered_questions
                            randomquizinstance.save()
                        if student.get_unanswered_questions(quiz).exists():
                            return redirect('students:take', pk)

            else:
                form = TakeQuizForm(question=question)

            return render(request, 'classroom/students/take_quiz_form.html', {
                'quiz': quiz,
                'question': question,
                'form': form,
                'progress': progress
            })

        else:
            correctanswercounter = StudentAnswer.objects.filter(quiz=quiz,student=student,answer__is_correct=True).count()

            score = (correctanswercounter / 30) * 100
            TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
            return redirect('students:taken_quiz_list')


def retake(request,quizid,studentid):
    RandomQuiz.objects.filter(quiz_id=quizid,student_id=studentid).delete()
    TakenQuiz.objects.filter(quiz_id=quizid,student_id=studentid).delete()
    StudentAnswer.objects.filter(quiz_id=quizid,student_id=studentid).delete()
    return redirect('students:take', quizid)
