from django.db.models import Q
from .models import Employee


class EmployeeRepository : 
    def get_all(self):
        return Employee.objects.select_related("department").all()

    def search(self, text) :
        return Employee.objects.select_related("department").filter(
            Q(first_name__icontains=text)
            | Q(last_name__icontains=text)
            | Q(email__icontains=text)
        )

    def email_exists(self, email) :
        return Employee.objects.filter(email=email).exists()

    def save(self, **data):
        return Employee.objects.create(**data)