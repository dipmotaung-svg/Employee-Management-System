from multiprocessing import context

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from urllib3 import request


class EmployeeListView(LoginRequiredMixin, View):
    service = None   # filled in from urls.py

    def get(self, request):
        search = request.GET.get("q", "")
        department = request.GET.get("department", "")
        employee_type = request.GET.get("employee_type", "")
        status = request.GET.get("status", "")

        context = { 
            "employees": self.service.list_employees(search, department, employee_type, status),
            "summary": self.service.get_dashboard_summary(),
            "departments": self.service.get_departments(),
            "employee_types": self.service.get_employee_types(),
            "search": search,
            "selected_department": department,
            "selected_employee_type": employee_type,
            "selected_status": status,
        }

        return render(request, "employees/employee_list.html", context)