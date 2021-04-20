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
