from django import forms
from django.core.exceptions import ValidationError
from .models import Record, RecordType, RecordStatus, RecordCategory, RecordSubcategory

class DateInput(forms.DateInput):
    input_type = 'date'

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = True
        self.fields['type'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True

        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['subcategory'].widget.attrs.update({'class': 'form-select'})

        self.fields['status'].empty_label = 'Выберите статус'
        self.fields['type'].empty_label = 'Выберите тип'
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['subcategory'].empty_label = 'Выберите подкатегорию'

        self.fields['category'].queryset = RecordCategory.objects.all()
        self.fields['subcategory'].queryset = RecordSubcategory.objects.all()

        if self.is_bound:
            type_id = self.data.get('type')
            category_id = self.data.get('category')
            if type_id:
                self.fields['category'].queryset = RecordCategory.objects.filter(type_id=type_id)
            if category_id:
                self.fields['subcategory'].queryset = RecordSubcategory.objects.filter(category_id=category_id)
        elif self.instance.pk:
            self.fields['category'].queryset = RecordCategory.objects.filter(type=self.instance.type)
            self.fields['subcategory'].queryset = RecordSubcategory.objects.filter(category=self.instance.category)

    def clean(self):
        cleaned_data = super().clean()
        record_type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if category and record_type and category.type != record_type:
            raise ValidationError('Категория должна относиться к выбранному типу.')
        if subcategory and category and subcategory.category != category:
            raise ValidationError('Подкатегория должна относиться к выбранной категории.')

        return cleaned_data

class RecordTypeForm(forms.ModelForm):
    class Meta:
        model = RecordType
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class RecordStatusForm(forms.ModelForm):
    class Meta:
        model = RecordStatus
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class RecordCategoryForm(forms.ModelForm):
    class Meta:
        model = RecordCategory
        fields = ['type', 'name']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RecordSubcategoryForm(forms.ModelForm):
    class Meta:
        model = RecordSubcategory
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RecordFilterForm(forms.Form):
    date_from = forms.DateField(required=False, widget=DateInput(attrs={'class': 'form-control'}))
    date_to = forms.DateField(required=False, widget=DateInput(attrs={'class': 'form-control'}))
    status = forms.ModelChoiceField(queryset=RecordStatus.objects.all(), required=False, empty_label='Выберите статус', widget=forms.Select(attrs={'class': 'form-select'}))
    type = forms.ModelChoiceField(queryset=RecordType.objects.all(), required=False, empty_label='Выберите тип', widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=RecordCategory.objects.all(), required=False, empty_label='Выберите категорию', widget=forms.Select(attrs={'class': 'form-select'}))
    subcategory = forms.ModelChoiceField(queryset=RecordSubcategory.objects.all(), required=False, empty_label='Выберите подкатегорию', widget=forms.Select(attrs={'class': 'form-select'}))
