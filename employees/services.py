class EmployeeService:
    def __init__(self, repository):
        self.repository = repository

    def list_employees(self, search_text = ""):
        search_text = search_text.strip()
        if search_text:
            return self.repository.search(search_text)
        return self.repository.get_all()

    def create_employee(self, **data):
        data["email"] = data["email"].strip().lower()
        if self.repository.email_exists(data["email"]):
            raise ValueError("An employee with this email already exists.")
        return self.repository.save(**data)

    