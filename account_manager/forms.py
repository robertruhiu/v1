from django import forms

from account_manager.models import Shortlist

ACTION_CHOICES = [
    ('shortlist', 'shortlist'),
    ('reject', 'reject'),
]


class ShortlistRejectForm(forms.Form):
    action = forms.CharField(widget=forms.Select(choices=ACTION_CHOICES))


class ShortlistCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Shortlist
        fields = ['title', 'category']


class ShortlistUpdateForm(forms.ModelForm):
    class Meta:
        model = Shortlist
        fields = ['title', 'category']


class ShortlistDeleteForm(forms.ModelForm):
    class Meta:
        model = Shortlist
        fields = '__all__'


class ListForm(forms.Form):
    lists = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                      choices=Shortlist.objects.all().values_list('id', 'title'))


class DevEmailForm(forms.Form):
    subject = forms.CharField(max_length=200, widget=forms.TextInput,
                              initial='[Action Required] Update your Codeln Profile')
    message = forms.CharField(max_length=2000, widget=forms.Textarea,
                              initial='You have an incomplete developer profile on Codeln.'
                                      'There are new and exciting Job opportunities every week on Codeln.'
                                      'Update your profile to participate in recruitment drives')


class InviteToJobForm(forms.Form):
    url = forms.CharField(max_length=240, widget=forms.TextInput, initial='https://www.codeln.com/jobdetails/441')
    subject = forms.CharField(max_length=200, widget=forms.TextInput,
                              initial='[Action Required] Job Match on Codeln')
    message = forms.CharField(max_length=2000, widget=forms.Textarea,
                              initial='<p>Hi,</p>'
                                      ' <p> This is Dexter from Codeln</p>'
                                      '<p>I hope you are doing good.</p>'
                                      '<p>Please find here this new job offer.</p>'
                                      '<p>COUNTRY: Ghana | City : Accra</p>'
                                      '<p>CONTRACT TYPE: FULL TIME AT THE OFFICE</p>'
                                      '<p>SKILL SET : REACT / NODEJS</p>'
                                      '<p>YEARS OF EXPERIENCE: > 3+ years of experience as a MERN Developer</p>'
                                      '<p>SALARY: USD 800 - 1500</p>'
                                      '<p>COMPANY : RAZOR GRIP We have been working for years on innovative,'
                                      'interesting '
                                      'and challenging projects focusing on the most advancedtechnologies (among the '
                                      'first to take on Node.JS and Angular for Enterprise development).'
                                      'We also have extensive experience in managing systems, '
                                      'outsourcing andproviding IT services and solutions.</p>'
                                      '<p>Our customers enjoy maximized production at minimum time and at predictable '
                                      'costs.</p> '
                                      '<p>Please find here more information</p>'
                                      '<p>It\'s a remote and full time role. Let me know if you are interested and '
                                      'apply online | REACT / NODEJS.</p>')
