from fastapi.security import HTTPBearer


SECURITY_BEARER = HTTPBearer()
SECURITY_BEARER.auto_error = False


from .auth_controller import auth_router
