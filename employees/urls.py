from django.urls import path 
from .repositories import EmployeeRepository
from .services import EmployeeService
from .views import EmployeeListView, EmpoyeeListView

repository = EmployeeRepository()
service = EmployeeService(repository)

urlpatterns = [
    path("", EmployeeListView.as_view(service=service), name="employee_list"),
]

