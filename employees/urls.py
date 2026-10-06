from django.urls import path

from employees.repositories.employee_repository import EmployeeRepository
from employees.services.employee_service import EmployeeService
from employees.views import EmployeeListView, hello

app_name = "employees"

repository = EmployeeRepository()
service = EmployeeService(repository)

urlpatterns = [
    path("", EmployeeListView.as_view(service=service), name="employee_list"),
    path("hello/", hello, name="hello"),
]