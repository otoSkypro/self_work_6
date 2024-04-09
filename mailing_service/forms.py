# mailing_service/forms.py
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import Client, Mailing, Message
from django.forms import TimeInput
from django import forms


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Клиент с такой почтой уже существует.")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if Client.objects.filter(full_name=full_name).exists():
            raise forms.ValidationError("Клиент с таким именем уже существует.")
        return full_name


class ClientDeleteConfirmationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = []


class MailingForm(forms.ModelForm):
    time_of_day = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Mailing
        fields = ['title', 'content', 'clients', 'start_time', 'end_time', 'frequency', 'status', 'time_of_day']
        widgets = {
            'start_time': DateTimePickerInput(),
            'end_time': DateTimePickerInput(),
            'time_of_day': TimeInput(attrs={'class': 'form-control datetimepicker'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("Дата начала не может быть позже даты окончания.")


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
