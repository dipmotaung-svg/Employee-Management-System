from django.contrib import admin
from .models import Department, Employee

admin.site.register(Department)
admin.site.register(Employee)

admin.site.site_header = "SkillBridge EMS Administration"
admin.site.site_title = "SkillBridge EMS Admin"
admin.site.index_title = "Manage employees and departments"