from django.db.models import Q
from employees.models import Department, Employee

class EmployeeRepository:
    def filter(
        self,
        search="",
        department_id=None,
        employee_type="",
        is_active=None
    ):

        employees = Employee.objects.select_related(
            "department"
        ).all()

        if search:
            employees = employees.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(employee_id__icontains=search)
            )

        if department_id:
            employees = employees.filter(
                department_id=department_id
            )


        if employee_type:
            employees = employees.filter(
                employee_type=employee_type
            )

        if is_active is not None:
            employees = employees.filter(
                is_active=is_active
            )

        return employees.order_by(
            "last_name",
            "first_name"
        )

    def count_all(self):
        return Employee.objects.count()

    def count_active(self):
        return Employee.objects.filter(
            is_active=True
        ).count()

    def count_inactive(self):
        return Employee.objects.filter(
            is_active=False
        ).count()


    def count_departments(self):
        return Department.objects.count()

    def get_departments(self):
        return Department.objects.all().order_by(
            "name"
        )

    def get_employee_types(self):
        return Employee.EMPLOYEE_TYPE

    def email_exists(self, email):
        return Employee.objects.filter(email__iexact=email).exists()

    def save(self, **data):
        return Employee.objects.create(**data)
