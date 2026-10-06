from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


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
                search,
                department,
                employee_type,
                status
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