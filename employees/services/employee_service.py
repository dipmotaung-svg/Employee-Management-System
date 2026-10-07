class EmployeeService:
    def __init__(self, repository):
        self.repository = repository

    def list_employees(self, search_text="", department="", employee_type="", status=""):
        try:
            department_id = int(department) if department else None
        except ValueError:
            department_id = None

        is_active = None
        if status == "active":
            is_active = True
        elif status == "inactive":
            is_active = False

        return self.repository.filter(
            search=search_text.strip(),
            department_id=department_id,
            employee_type=employee_type,
            is_active=is_active,
        )

    def get_dashboard_summary(self):
        return {
            "total_employees": self.repository.count_all(),
            "active_employees": self.repository.count_active(),
            "inactive_employees": self.repository.count_inactive(),
            "department_count": self.repository.count_departments(),
        }

    def get_departments(self):
        return self.repository.get_departments()

    def get_employee_types(self):
        return self.repository.get_employee_types()

    def get_employee(self, pk):
        return self.repository.get_by_id(pk)

    def create_employee(self, form):
        data = form.cleaned_data
        if self.repository.email_exists(data["email"]):
            form.add_error("email", "An employee with this email already exists.")
            return None
        if self.repository.employee_id_exists(data["employee_id"]):
            form.add_error("employee_id", "This employee ID is already in use.")
            return None
        return self.repository.save(form.save(commit=False))

    def update_employee(self, pk, form):
        data = form.cleaned_data
        if self.repository.email_exists(data["email"], exclude_id=pk):
            form.add_error("email", "Another employee already has this email.")
            return None
        if self.repository.employee_id_exists(data["employee_id"], exclude_id=pk):
            form.add_error("employee_id", "Another employee already has this ID.")
            return None
        return self.repository.update(form.save(commit=False))

    def delete_employee(self, pk):
        employee = self.repository.get_by_id(pk)
        if employee:
            self.repository.delete(employee)
        return employee