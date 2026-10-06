from django import forms
from django.utils.crypto import constant_time_compare

from .models import Employee


class LoginForm(forms.Form):
    employee_no = forms.CharField(
        label='従業員番号',
        max_length=6,
        error_messages={
            'required': '従業員番号を入力してください。',
            'max_length': '従業員番号は6文字以内で入力してください。',
        },
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='パスワード',
        strip=False,
        error_messages={'required': 'パスワードを入力してください。'},
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        employee_no = cleaned_data.get('employee_no')
        password = cleaned_data.get('password')
        if employee_no and password:
            employee = Employee.objects.filter(employee_no=employee_no).first()
            if employee is None or not constant_time_compare(password, employee.password):
                raise forms.ValidationError('従業員番号またはパスワードが違います。')
            self.employee = employee
        return cleaned_data
