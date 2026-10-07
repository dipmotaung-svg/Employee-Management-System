from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from .forms import EmployeeForm
from .decorators import audit_log

def hello(request):
    return render(request, "employees/hello.html")


class EmployeeListView(LoginRequiredMixin, View):
    service = None

    def get(self, request):
        search = request.GET.get("q", "")
        department = request.GET.get("department", "")
        employee_type = request.GET.get("employee_type", "")
        status = request.GET.get("status", "")

        context = {
            "employees": self.service.list_employees(
                search, department, employee_type, status
            ),
            "summary": self.service.get_dashboard_summary(),
            "departments": self.service.get_departments(),
            "employee_types": self.service.get_employee_types(),
            "search": search,
            "selected_department": department,
            "selected_employee_type": employee_type,
            "selected_status": status,
        }

        return render(request, "employees/employee_list.html", context)


class EmployeeCreateView(LoginRequiredMixin, View):
    service = None

    def get(self, request):
        return render(request, "employees/employee_form.html",
                    {"form": EmployeeForm(), "title": "Add employee"})
    @audit_log("CREATE")
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = self.service.create_employee(form)
            if employee:
                messages.success(request, "Employee created.")
                return redirect("employees:employee_detail", pk=employee.pk)
        return render(request, "employees/employee_form.html",
                    {"form": form, "title": "Add employee"})


class EmployeeDetailView(LoginRequiredMixin, View):
    service = None

    def get(self, request, pk):
        employee = self.service.get_employee(pk)
        if not employee:
            raise Http404
        return render(request, "employees/employee_detail.html", {"employee": employee})


class EmployeeUpdateView(LoginRequiredMixin, View):
    service = None

    def get(self, request, pk):
        employee = self.service.get_employee(pk)
        if not employee:
            raise Http404
        return render(request, "employees/employee_form.html",
                    {"form": EmployeeForm(instance=employee), "title": "Edit employee"})

    @audit_log("UPDATE")
    def post(self, request, pk):
        employee = self.service.get_employee(pk)
        if not employee:
            raise Http404
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            if self.service.update_employee(pk, form):
                messages.success(request, "Employee updated.")
                return redirect("employees:employee_detail", pk=pk)
        return render(request, "employees/employee_form.html",
                    {"form": form, "title": "Edit employee"})


class EmployeeDeleteView(LoginRequiredMixin, View):
    service = None

    def get(self, request, pk):
        employee = self.service.get_employee(pk)
        if not employee:
            raise Http404
        return render(request, "employees/employee_confirm_delete.html", {"employee": employee})

    @audit_log("DELETE")
    def post(self, request, pk):
        self.service.delete_employee(pk)
        messages.success(request, "Employee deleted.")
        return redirect("employees:employee_list")