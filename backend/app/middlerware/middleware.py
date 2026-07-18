from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from backend.app.core.security import verify_session_token
from datetime import datetime
import time


OPEN_PATHS = ["/auth/login", "/auth/register", "/docs", "/openapi.json", "/redoc"]



class Middlerware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"DEBUG PATH: '{request.url.path}'") 

        if request.url.path in OPEN_PATHS:
            start = time.time()
            responce = await call_next(request)
            end = time.time()
            print("Time: ", end - start)
            return responce

        
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Token missing"
                }
            )
        
        token = auth_header.split(" ")[1]

        token_entry = verify_session_token(
            token
        )
        
        if not token_entry:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid token"
                }
            )
        
        exp_time = datetime.utcfromtimestamp(token_entry['exp'])
        if exp_time < datetime.utcnow():
                return JSONResponse(status_code=401, content={"detail": "Token expired"})
        
        return await call_next(request)
    

