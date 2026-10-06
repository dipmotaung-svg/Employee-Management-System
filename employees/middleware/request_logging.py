import logging
import time

logger = logging.getLogger("ems.requests")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()

        response = self.get_response(request)

        duration_ms = (time.perf_counter() - start) * 1000
        user = request.user.username if request.user.is_authenticated else "anonymous"

        logger.info(
            "%s %s | user=%s | status=%s | %.1fms",
            request.method, request.path, user, response.status_code, duration_ms,
        )
        response["X-Response-Time-ms"] = f"{duration_ms:.1f}"
        return response

    def process_exception(self, request, exception):
        logger.error(
            "EXCEPTION %s %s | Error: %s",
            request.method, request.path, exception, exc_info=True,
        )
        return None