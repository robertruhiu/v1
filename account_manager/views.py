from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from account_manager.models import Shortlist
from accounts.models import Profile

from account_manager.filters import DevFilter

# Create your views here.
# @login_required
def index(request):
    query = request.GET.get('q', None)
    lists = Shortlist.objects.all()
    if not query:
        devs = Profile.objects.filter(user_type='developer')
        devs_filter = DevFilter(request.GET, queryset=devs)
        devs = DevFilter(request.GET, queryset=devs).qs
        return render(request, 'account_manager/dashboard.html', {'devs_filter': devs_filter, 'devs': devs, 'lists': lists})
    else:
        devs = Profile.objects.search(query)
        return render(request, 'account_manager/dashboard.html', {'devs': devs, 'lists': lists})

