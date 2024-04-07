# catalog/forms.py
from .models import Product
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Version


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))


class EditVersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_active']

    def __init__(self, *args, **kwargs):
        super(EditVersionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'publish_status']  # Добавляем поле publish_status

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        name = self.cleaned_data['name'].lower()
        for word in forbidden_words:
            if word in name:
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии продукта.')
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        description = self.cleaned_data['description'].lower()
        for word in forbidden_words:
            if word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено в описании продукта.')
        return description
