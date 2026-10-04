from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class EmployeeListView(LoginRequiredMixin, View):
    service = None   # filled in from urls.py

    def get(self, request):
        search = request.GET.get("q", "")
        employees = self.service.list_employees(search)
        return render(request, "employees/employee_list.html",
                        {"employees": employees, "search": search})