from django.core.cache import cache
from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from employees.models import Employee


from .notifications import notify_employee_change
from .forms import EmployeeForm
from .decorators import audit_log



@login_required
@require_GET
def employee_api(request):
    search = request.GET.get("search", "").strip()

    employees = Employee.objects.select_related("department").all()

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    data = []

    for employee in employees:
        data.append({
            "id": employee.pk,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "department": (
                employee.department.name
                if employee.department else None
            ),
        })

    return JsonResponse({
        "count": len(data),
        "employees": data,
    })


@login_required
@require_GET
def employee_api_detail(request, pk):
    employee = Employee.objects.select_related(
        "department"
    ).filter(pk=pk).first()

    if employee is None:
        raise Http404("Employee not found")

    return JsonResponse({
        "id": employee.pk,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "department": (
            employee.department.name
            if employee.department else None
        ),
        "employee_type": employee.employee_type,
        "is_active": employee.is_active,
    })


@login_required
@require_GET
def employee_api_stats(request):
    return JsonResponse({
        "total": Employee.objects.count(),
        "active": Employee.objects.filter(is_active=True).count(),
        "inactive": Employee.objects.filter(is_active=False).count(),
    })

@login_required
@require_POST
def clear_cache(request):
    cache.delete("employee_dashboard_summary")

    messages.success(
        request,
        "Cache cleared successfully."
    )

    return redirect("employees:employee_list")

def hello(request):
    return render(request, "employees/hello.html")



class EmployeeListView(LoginRequiredMixin, View):
    service = None
    def get(self, request):
        filter_names = ("q", "department", "employee_type", "status")
        
        if request.GET.get("reset") == "1":
            for name in filter_names:
                request.session.pop(f"employee_filter_{name}", None)
        elif any(name in request.GET for name in filter_names):
            for name in filter_names:
                request.session[f"employee_filter_{name}"] = request.GET.get(name, "")
        
        search = request.session.get("employee_filter_q", "")
        department = request.session.get("employee_filter_department", "")
        employee_type = request.session.get("employee_filter_employee_type", "")
        status = request.session.get("employee_filter_status", "")
        recent_ids = request.session.get("recently_viewed", [])
        recent_employees = Employee.objects.filter(
            pk__in=recent_ids
        )
        recent_lookup = {
            employee.pk: employee
            for employee in recent_employees
        }
        recently_viewed = [
            recent_lookup[employee_id]
            for employee_id in recent_ids
            if employee_id in recent_lookup
        ]
        summary = cache.get("employee_dashboard_summary")
        if summary is None:
            summary = self.service.get_dashboard_summary()
            cache.set("employee_dashboard_summary", summary, timeout=60)
        context = {
            "employees": self.service.list_employees(
                search, department, employee_type, status
            ),
            "summary": summary,
            "departments": self.service.get_departments(),
            "employee_types": self.service.get_employee_types(),
            "search": search,
            "selected_department": department,
            "selected_employee_type": employee_type,
            "selected_status": status,
            "recently_viewed": recently_viewed,
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
                transaction.on_commit(
                    lambda: (
                        cache.delete("employee_dashboard_summary"),
                        notify_employee_change()
                    )
                )
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
        recently_viewed = request.session.get("recently_viewed", [])
        recently_viewed = [
            employee_id for employee_id in recently_viewed
            if employee_id != employee.pk
        ]
        recently_viewed.insert(0, employee.pk)
        request.session["recently_viewed"] = recently_viewed[:5]
        recent_ids = request.session["recently_viewed"]
        recent_employees = Employee.objects.filter(
            pk__in=recent_ids
        )
        recent_lookup = {
            employee.pk: employee
            for employee in recent_employees
        }
        recently_viewed_employees = [
            recent_lookup[employee_id]
            for employee_id in recent_ids
            if employee_id in recent_lookup
        ]
        return render(request, "employees/employee_detail.html",
        {"employee": employee, "recently_viewed": recently_viewed_employees,})


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
                transaction.on_commit(
                    lambda: (
                        cache.delete("employee_dashboard_summary"),
                        notify_employee_change()
                    )
                )
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
        employee = self.service.get_employee(pk)
        if not employee:
            raise Http404
        full_name = f"{employee.first_name} {employee.last_name}"
        self.service.delete_employee(pk)
        transaction.on_commit(
            lambda: (
                cache.delete("employee_dashboard_summary"),
                notify_employee_change()
            )
        )
        messages.success(
            request,
            f"{full_name} has been deleted successfully."
        )
        return redirect("employees:employee_list")