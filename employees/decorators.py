import logging
from functools import wraps
from pathlib import Path

from django.conf import settings

logger = logging.getLogger("employees.audit")

if not logger.handlers:
    log_dir = Path(settings.BASE_DIR) / "logs"
    log_dir.mkdir(exist_ok=True)
    handler = logging.FileHandler(log_dir / "audit.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def audit_log(action):
    def decorator(method):
        @wraps(method)
        def wrapper(self, request, *args, **kwargs):
            response = method(self, request, *args, **kwargs)
            # A redirect means the action succeeded
            if response.status_code in (301, 302):
                logger.info(
                    "user=%s | action=%s | employee_pk=%s",
                    request.user.username,
                    action,
                    kwargs.get("pk", "new"),
                )
            return response
        return wrapper
    return decorator