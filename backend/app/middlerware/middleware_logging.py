import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("request_logger")
logging.basicConfig(level=logging.INFO)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        log_id = str(uuid.uuid4())
        start = time.time()

        # request state me daal do, taaki routes/exception handlers me bhi use ho sake
        request.state.log_id = log_id

        logger.info(f"[{log_id}] START {request.method} {request.url.path}")

        response = await call_next(request)

        duration = round((time.time() - start) * 1000, 2)  # ms me
        logger.info(
            f"[{log_id}] END {request.method} {request.url.path} "
            f"status={response.status_code} time={duration}ms"
        )

        # response header me bhi bhej do — debugging ke liye useful hota hai
        response.headers["X-Log-ID"] = log_id
        response.headers["X-Process-Time-ms"] = str(duration)

        return response