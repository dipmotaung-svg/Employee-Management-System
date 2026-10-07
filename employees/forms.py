import datetime

from django import forms
from employees.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee

        fields = [
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "department",
            "title",
            "employee_type",
            "salary",
            "date_joined",
            "is_active",
        ]

        labels = {
            "employee_id": "Employee ID",
            "phone_number": "Phone number",
            "title": "Job title",
            "employee_type": "Employee type",
            "date_joined": "Date joined",
            "is_active": "Currently active",
        }

        help_texts = {
            "employee_id": "Exactly 13 letters or numbers.",
            "phone_number": "Optional. Digits, spaces and + only.",
            "salary": "Monthly salary in rand, for example 25000.00",
        }

        widgets = {
            "date_joined": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def clean_employee_id(self):
        value = self.cleaned_data["employee_id"].strip()

        if len(value) != 13 or not value.isalnum():
            raise forms.ValidationError(
                "Employee ID must be exactly 13 letters or numbers."
            )

        return value

    def clean_first_name(self):
        return self.cleaned_data["first_name"].strip().title()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].strip().title()

    def clean_phone_number(self):
        value = self.cleaned_data.get("phone_number", "").strip()

        if value and not value.replace(" ", "").replace("+", "").isdigit():
            raise forms.ValidationError(
                "Phone number can only contain digits, spaces and +."
            )

        return value

    def clean_salary(self):
        value = self.cleaned_data["salary"]

        if value <= 0:
            raise forms.ValidationError(
                "Salary must be greater than zero."
            )

        return value

    def clean_date_joined(self):
        value = self.cleaned_data["date_joined"]

        if value > datetime.date.today():
            raise forms.ValidationError(
                "Date joined cannot be in the future."
            )

        return value