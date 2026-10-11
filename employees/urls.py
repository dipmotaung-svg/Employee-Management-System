from django.urls import path

from employees.repositories.employee_repository import EmployeeRepository
from employees.services.employee_service import EmployeeService
from employees.views import (
    EmployeeListView, EmployeeCreateView, EmployeeDetailView,
    EmployeeUpdateView, EmployeeDeleteView, hello,
    employee_api, clear_cache,
)

app_name = "employees"

repository = EmployeeRepository()
service = EmployeeService(repository)

urlpatterns = [
    path("", EmployeeListView.as_view(service=service), name="employee_list"),
    path("create/", EmployeeCreateView.as_view(service=service), name="employee_create"),
    path("<int:pk>/", EmployeeDetailView.as_view(service=service), name="employee_detail"),
    path("<int:pk>/edit/", EmployeeUpdateView.as_view(service=service), name="employee_edit"),
    path("<int:pk>/delete/", EmployeeDeleteView.as_view(service=service), name="employee_delete"),
    path("hello/", hello, name="hello"),
    path("api/employees/", employee_api, name="employee_api"),
    path("clear-cache/", clear_cache, name="clear_cache"),
]

