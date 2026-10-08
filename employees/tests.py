
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from employees.forms import EmployeeForm
from employees.models import Department, Employee
from employees.repositories.employee_repository import EmployeeRepository
from employees.services.employee_service import EmployeeService


class EmployeeTests(TestCase):

    def setUp(self):
        # Create sample data in Django's separate test database.
        self.department = Department.objects.create(name="IT")

        self.employee = Employee.objects.create(
            employee_id="EMP0000000001",
            first_name="Xolisa",
            last_name="Mokoena",
            email="xolisa@example.com",
            phone_number="0712345678",
            department=self.department,
            title="Developer",
            employee_type="full_time",
            salary=Decimal("25000.00"),
            date_joined=date(2025, 1, 15),
            is_active=True,
        )

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        self.repository = EmployeeRepository()
        self.service = EmployeeService(self.repository)

    def employee_data(self):
        # Valid data for testing the employee form.
        return {
            "employee_id": "EMP0000000002",
            "first_name": "Lebo",
            "last_name": "Dlamini",
            "email": "lebo@example.com",
            "phone_number": "0723456789",
            "department": str(self.department.pk),
            "title": "Tester",
            "employee_type": "intern",
            "salary": "12000.00",
            "date_joined": "2025-02-01",
            "is_active": "on",
        }





    def test_valid_employee_form(self):
        form = EmployeeForm(data=self.employee_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_employee_id(self):
        data = self.employee_data()
        data["employee_id"] = "123"
        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("employee_id", form.errors)

    def test_negative_salary_rejected(self):
        data = self.employee_data()
        data["salary"] = "-500"
        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("salary", form.errors)

    def test_future_join_date_rejected(self):
        data = self.employee_data()
        data["date_joined"] = "2099-01-01"
        form = EmployeeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("date_joined", form.errors)







    def test_employee_search(self):
        results = self.service.list_employees(search_text="Xolisa")

        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.employee)

    def test_dashboard_statistics(self):
        summary = self.service.get_dashboard_summary()

        self.assertEqual(summary["total_employees"], 1)
        self.assertEqual(summary["active_employees"], 1)
        self.assertEqual(summary["inactive_employees"], 0)
        self.assertEqual(summary["department_count"], 1)




    

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("employees:employee_list")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_create_requires_login(self):
        response = self.client.get(
            reverse("employees:employee_create")
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_requires_login(self):
        response = self.client.post(
            reverse(
                "employees:employee_delete",
                args=[self.employee.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Employee.objects.filter(pk=self.employee.pk).exists()
        )






    def test_logged_in_user_can_view_dashboard(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("employees:employee_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Xolisa")

    def test_create_employee_workflow(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("employees:employee_create"),
            data=self.employee_data(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Employee.objects.filter(
                employee_id="EMP0000000002"
            ).exists()
        )

    def test_update_employee_workflow(self):
        self.client.force_login(self.user)

        data = self.employee_data()
        data["employee_id"] = self.employee.employee_id
        data["email"] = self.employee.email
        data["first_name"] = "Updated"

        response = self.client.post(
            reverse(
                "employees:employee_edit",
                args=[self.employee.pk],
            ),
            data=data,
        )

        self.assertEqual(response.status_code, 302)

        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, "Updated")

    def test_delete_employee_workflow(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "employees:employee_delete",
                args=[self.employee.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Employee.objects.filter(pk=self.employee.pk).exists()
        )
