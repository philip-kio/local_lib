from django import forms 


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text= 'Enter a date between now and 4 weeeks (default 3).')




    def clean_renew_date(self):
        data = self.cleaned_data['renewal_date']

        # check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # check if a date is in the allowed range (+4 weeks from today).
        if data > datetim.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_ ('Invalid date - renewal more than 4 weeks'))


        # remember to always return the cleaned data

        return data