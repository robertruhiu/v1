from frontend.models import Job, Profile

import django_filters


MONTH_CHOICES = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)
class JobFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='created', lookup_expr='year')
    month = django_filters.ChoiceFilter( choices= MONTH_CHOICES, field_name='created', lookup_expr='month')

    class Meta:
        model = Job
        fields = ['company', 'title', 'city', 'job_role',
                  'engagement_type', 'tech_stack', 'year', 'month',]


class DevFilter(django_filters.FilterSet):

    class Meta:
        model = Profile
        # fields = ['user','language', 'framework', 'skills', 'verified_skills', 'availabilty', 'gender', ]
        fields = ['language', 'framework', 'skills', 'verified_skills', 'availabilty', 'gender', ]

class ShortlistDevFilter(django_filters.FilterSet):

    class Meta:
        model = Profile
        # fields = ['user','language', 'framework', 'skills', 'verified_skills', 'availabilty', 'gender', ]
        fields = [ 'framework', 'skills', 'verified_skills', 'availabilty', 'gender', ]