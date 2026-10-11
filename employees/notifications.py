from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify_employee_change():
    channel_layer = get_channel_layer()

    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "employee_updates",
        {
            "type": "employee.updated",
            "message": (
                "Employee records have changed. "
                "Refresh the dashboard to see the latest information."
            ),
        }
    )