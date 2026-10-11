"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import include, path
from employees.views import (
    employee_api,
    employee_api_detail,
    employee_api_stats,
)



def home(request):
    return redirect("employees:employee_list")


urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path(
        "employees/",
        include("employees.urls")
    ),

    path("api/v1/employees/", employee_api, name="api_employee_list"),
    path("api/v1/employees/stats/", employee_api_stats, name="api_employee_stats"),
    path("api/v1/employees/<int:pk>/", employee_api_detail, name="api_employee_detail"),
    
    path(
        "",
        home,
        name="home"
    ),

]