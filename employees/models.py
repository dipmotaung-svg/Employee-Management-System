from django.db import models

# Create your models here.
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length = 20, unique = True)

    def __str__(self):
        return self.name    

class Employee(models.Model):
    EMPLOYEE_TYPE = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("intern", "Intern"),
    ]

    employee_id = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    title = models.CharField(max_length=50)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"