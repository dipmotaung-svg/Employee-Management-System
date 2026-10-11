from django.urls import path
from .consumers import EmployeeNotificationConsumer

websocket_urlpatterns = [
    path(
        "ws/employees/",
        EmployeeNotificationConsumer.as_asgi()
    ),
]