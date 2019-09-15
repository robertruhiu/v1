from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from classroom.models import TakenQuiz,Student

def changequiz(request):
    allstudents = Student.objects.all()
    alltakenquizes = TakenQuiz.objects.all()
    for onequiz in alltakenquizes:
        for onestudent in allstudents:
            if onestudent.user.id == onequiz.student.user.id:
                onequiz.student = onestudent.user
                onequiz.save()
    return render(request, 'frontend/landing.html')




