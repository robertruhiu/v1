import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from django.urls import reverse, reverse_lazy
from requests import Response
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status
from xhtml2pdf import pisa

from marketplace.models import Job, Profile, JobApplication
from account_manager.models import Shortlist
from account_manager.filters import JobFilter, DevFilter, ShortlistDevFilter
from account_manager.forms import ShortlistCreateUpdateForm, ListForm

# Create your views here.
# dashboard
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def index(request):
    query = request.GET.get('q', None)
    lists = Shortlist.objects.all()
    list_form = ListForm()
    if not query:
        all_devs = Profile.objects.filter(user_type='developer')
        devs_filter = DevFilter(request.GET, queryset=all_devs)
        devs = DevFilter(request.GET, queryset=all_devs).qs
        page = request.GET.get('page', 1)
        paginator = Paginator(devs, 25)
        try:
            devs = paginator.page(page)
        except PageNotAnInteger:
            devs = paginator.page(1)
        except EmptyPage:
            devs = paginator.page(paginator.num_pages)
        return render(request, 'account_manager/dashboard.html',
                      {'devs': devs, 'lists': lists, 'devs_filter': devs_filter, 'list_form':list_form})
    else:
        search_results = Profile.objects.search(query)
        devs_filter = DevFilter(request.GET, queryset=search_results)
        devs = DevFilter(request.GET, queryset=search_results).qs
        page = request.GET.get('page', 1)

        paginator = Paginator(devs, 25)
        try:
            devs = paginator.page(page)
        except PageNotAnInteger:
            devs = paginator.page(1)
        except EmptyPage:
            devs = paginator.page(1)

        return render(request, 'account_manager/dashboard.html', {'devs': devs, 'lists': lists,
                                                                  'devs_filter': devs_filter, 'list_form': list_form})


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
def cv(request, id):
    dev = Profile.objects.get(id=id)
    return render(request, 'account_manager/cv.html', {'dev': dev})
    # return render(request, 'account_manager/full_cv.html', {'dev': dev})
    # return render(request, 'account_manager/stripped_cv.html', {'dev': dev})




import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def download_cv(request, id):
    template_path = 'account_manager/full_cv.html'
    dev = Profile.objects.get(id=id)
    context = {'dev': dev}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # filename = f'{dev.user.first_name} {dev.user.last_name}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{dev.user.first_name} {dev.user.last_name}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def download_stripped_cv(request, id):
    template_path = 'account_manager/stripped_cv.html'
    dev = Profile.objects.get(id=id)
    context = {'dev': dev}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{dev.user.first_name} {dev.user.last_name}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def shortlist(request, id):
    list = Shortlist.objects.get(id=id)
    devs = list.developers.all()
    devs_filter = ShortlistDevFilter(request.GET, queryset=devs)
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
            return redirect('account_manager:base')
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
        return redirect('account_manager:myjob', id=application.job.id)
    elif data == 'reject':
        application.stage = 'rejected'
        application.save()
        return redirect('account_manager:myjob', id=application.job.id)
    else:
        # todo return error messages
        return redirect('account_manager:myjob', id=application.job.id)


class ShortlistCreate(CreateView):
    template_name = 'account_manager/shortlist_form.html'
    model = Shortlist
    fields = ['title', 'category']
    success_url = '/cac/all_shortlist/'


class ShortlistUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'account_manager/shortlist_form.html'
    model = Shortlist
    fields = ['title', 'category']
    success_url = '/cac/all_shortlist/'


class ShortlistDelete(LoginRequiredMixin, DeleteView):
    template_name = 'account_manager/shortlist_confirm_delete.html'
    model = Shortlist
    success_url = '/cac/all_shortlist/'


