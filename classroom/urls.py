from django.urls import include, path

from .views import students, teachers
from classroom.views.students import AllQuizzes,TakeQuiz,QuizQuestions,PostAnswer,UpdateRandomquiz,CalculateScore,Taken,Subjects
urlpatterns = [
    path('allquizzes', AllQuizzes.as_view()),
    path('takequiz/<int:candidate>/<int:quiz>', TakeQuiz.as_view()),
    path('questions/<int:quiz>', QuizQuestions.as_view()),
    path('updaterandquiz/<int:pk>', UpdateRandomquiz.as_view()),
    path('postanswer', PostAnswer.as_view()),
    path('score/<int:candidate>/<int:quiz>', CalculateScore.as_view()),
    path('taken/<int:candidate>', Taken.as_view()),
    path('subjects', Subjects.as_view()),





    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take, name='take'),
        path('retake/<int:quizid>/<int:studentid>',students.retake, name='retake'),

    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
