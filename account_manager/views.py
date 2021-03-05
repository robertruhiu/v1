import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from django.urls import reverse
from requests import Response
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status

from marketplace.models import Job, Profile, JobApplication
from account_manager.models import Shortlist
from account_manager.filters import JobFilter, DevFilter
from account_manager.forms import ShortlistCreateUpdateForm, ListForm


# Create your views here.
# dashboard
from django.core.paginator import Paginator
@login_required
def index(request):
    query = request.GET.get('q', None)
    lists = Shortlist.objects.all()
    if not query:
        all_devs = Profile.objects.filter(user_type='developer')
        print(all_devs.count())
        paginator = Paginator(all_devs, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # devs_filter = DevFilter(request.GET, queryset=devs)
        # devs = DevFilter(request.GET, queryset=devs).qs
        return render(request, 'account_manager/dashboard.html', {'page_obj': page_obj, 'lists':lists})
    else:
        devs = Profile.objects.search(query)
        # print(devs.count())
        # paginator = Paginator(devs, 25)
        # page_number = request.GET.get('page')
        page_obj = devs
        return render(request, 'account_manager/dashboard.html', {'page_obj': page_obj, 'lists': lists})

# @login_required
# def index(request):
#     query = request.GET.get('q', None)
#     lists = Shortlist.objects.all()
#     if not query:
#         devs = Profile.objects.filter(user_type='developer')
#         print(devs.count())
#         devs_filter = DevFilter(request.GET, queryset=devs)
#         devs = DevFilter(request.GET, queryset=devs).qs
#         return render(request, 'account_manager/dashboard.html', {'devs_filter': devs_filter,
#                                                                            'devs': devs, 'lists': lists})
#     else:
#         devs = Profile.objects.search(query)
#         return render(request, 'account_manager/dashboard.html', {'devs': devs, 'lists': lists})


# # developers
# @login_required
# def devs(request):
#     if request.method == 'POST':
#         email = request.GET.get('email')
#         devs_filter = Profile.objects.annotate(search=SearchVector('user__email'), ).filter(search=email)
#         return render(request, 'frontend/account_manager/developers.html', {'devs': devs_filter})
#     else:
#         devs = Profile.objects.filter(user_type='developer')
#         devs_filter = DevFilter(request.GET, queryset=devs)
#         devs = DevFilter(request.GET, queryset=devs).qs
#         return render(request, 'frontend/account_manager/developers.html', {'devs_filter': devs_filter,
#                                                                             'devs': devs})

@login_required
def mydev(request, id):
    dev = Profile.objects.get(id=id)
    return render(request, 'account_manager/developer.html', {'dev': dev})


# jobs views
@login_required
def jobs(request):
    query = request.GET.get('q', None)
    if not query:
        jobs = Job.objects.all()
        jobs_filter = JobFilter(request.GET, queryset=jobs)
        jobs = jobs_filter.qs
        return render(request, 'account_manager/jobs.html', {'jobs_filter': jobs_filter,
                                                                      'jobs': jobs})
    else:
        jobs = Job.objects.search(query)
        return render(request, 'account_manager/jobs.html', {'jobs': jobs})

@login_required
def myjob(request, id):
    job = Job.objects.get(id=id)
    applications = JobApplication.objects.filter(job=job)
    new_applications = applications.filter(created__day=datetime.now().day)
    shortlist = applications.filter(stage='shortlisted')
    rejected = applications.filter(stage='rejected')

    return render(request, 'account_manager/job.html', {'job': job, 'applications': applications,
                                                                 'new_applications': new_applications,
                                                                 'shortlist': shortlist, 'rejected': rejected})


# lists
@login_required
def all_shortlist(request):
    lists = Shortlist.objects.all()
    return render(request, 'account_manager/all_shortlist.html', {'lists': lists})

@login_required
def cv(request):
    return render(request, 'account_manager/cv.html')

# from io import BytesIO
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter, landscape
# from reportlab.lib.pagesizes import A4


@login_required
def download_cv(request):
    # # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()
    #
    # # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer)
    #
    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100, 100, "Hello world.")
    #
    # # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()
    #
    # # FileResponse sets the Content-Disposition header so that browsers
    # # present the option to save the file.
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    return redirect('frontend:cv')


@login_required
def shortlist(request, id):
    list = Shortlist.objects.get(id=id)
    devs = list.developers.all()
    devs_filter = DevFilter(request.GET, queryset=devs)
    # list = Shortlist.objects.get(slug=slug)
    return render(request, 'account_manager/shortlist.html', {'list': list, 'devs_filter': devs_filter})


@login_required
def add_shortlist(request):
    if request.method == 'POST':
        shortlist_form = ShortlistCreateUpdateForm(data=request.POST)
        if shortlist_form.is_valid():
            new_list = shortlist_form.save(commit=False)
    else:
        shortlist_form = ShortlistCreateUpdateForm()
        return render(request, 'account_manager/shortlist_form.html', {'shortlist_form': shortlist_form})

@login_required
def add_to_list(request, id):
    developer = Profile.objects.get(id=id)
    if request.method == 'POST':
        list_form = ListForm(data=request.POST)
        list_form
        if list_form.is_valid():
            lists = list_form.cleaned_data['lists']
            for list in lists:
                shortlist = Shortlist.objects.get(id=int(list))
                shortlist.developers.add(developer)
                shortlist.save()
            return redirect('frontend:index')
    else:
        list_form = ListForm()
        return render(request, 'account_manager/addtolist.html', {'developer': developer, 'list_form': list_form})
@login_required
def send_mail(request, id):
    developer = Profile.objects.get(id=id)
    if request.method == 'POST':
        list_form = ListForm(data=request.POST)
        list_form
        if list_form.is_valid():
            lists = list_form.cleaned_data['lists']
            for list in lists:
                shortlist = Shortlist.objects.get(id=int(list))
                shortlist.developers.add(developer)
                shortlist.save()
            return redirect('frontend:index')
    else:
        list_form = ListForm()
        return render(request, 'account_manager/addtolist.html', {'developer': developer, 'list_form': list_form})

@login_required
def update_application(request):
    application = JobApplication.objects.get(id=request.GET.get('id'))
    data = request.GET.get('data')
    if data == 'shortlist':
        application.stage = 'shortlisted'
        application.save()
        return redirect('frontend:myjob', id=application.job.id)
    elif data == 'reject':
        application.stage = 'rejected'
        application.save()
        return redirect('frontend:myjob', id=application.job.id)
    else:
        # todo return error messages
        return redirect('frontend:myjob', id=application.job.id)


class ShortlistCreate(LoginRequiredMixin, CreateView):
    template_name = 'account_manager/shortlist_form.html'
    model = Shortlist
    fields = ['title', 'category']
    success_url = '/all_shortlist/'
    # form_class = ShortlistCreateUpdateForm


class ShortlistUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'account_manager/shortlist_form.html'
    model = Shortlist
    fields = ['title', 'category']
    success_url = '/all_shortlist/'


class ShortlistDelete(LoginRequiredMixin, DeleteView):
    template_name = 'account_manager/shortlist_confirm_delete.html'
    model = Shortlist
    success_url = '/all_shortlist/'


# # test pdf view
# from django.http import HttpResponse
# from django.views.generic import View
#
# # importing get_template from loader
# from django.template.loader import get_template
#
# # import render_to_pdf from util.py
# from api.utils import render_to_pdf
#
#
# # Creating our view, it is a class based view
# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         pdf = render_to_pdf('account_manager/test.html')
#
#         # rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')
