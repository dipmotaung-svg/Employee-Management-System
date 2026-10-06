class EmployeeService:
    def __init__(self, repository):
        self.repository = repository

    def list_employees(self, search_text = "", department="", employee_type="", status=""):
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
            search=search_text,
            department_id=department_id,
            employee_type=employee_type,
            is_active=is_active
        )

    def get_dashboard_summary(self):
        return{
            "total_employees": self.repository.count_all(),
            "active_employees": self.repository.count_active(),
            "inactive_employees": self.repository.count_innactive(),
            "department_count": self.repository.count_departments
        }


    def get_departments(self):
        return self.repository.get_departments()

    def get_employee_types(self):
        return self.repository.get_employee_types()

    def create_employee(self, **data):
        data["email"] = data["email"].strip().lower()
        if self.repository.email_exists(data["email"]):
            raise ValueError("An employee with this email already exists.")
        return self.repository.save(**data)

    