from fastapi import APIRouter, Depends
from api.config import settings
from api.auth.dto import LoginDTO
from api.auth.auth_service import AuthService
from api.auth.strategies import LoginStrategies


auth_router = APIRouter(prefix='/auth', tags=['Authentication'])


@auth_router.get('/google/login')
async def login_google():
    uri = (
        'https://accounts.google.com/o/oauth2/v2/auth?'
        + f'response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&'
        + f'redirect_uri={settings.GOOGLE_REDIRECT_URI}&'
        + 'scope=openid%20profile%20email&access_type=offline'
    )
    return {'uri': uri}


@auth_router.get('/google/token')
async def auth_google(code: str, auth_service: AuthService = Depends(AuthService)):
    credentials = LoginDTO(email='notmatter@email.com', password=code)
    token: str = await auth_service.login(credentials, LoginStrategies.GOOGLE)
    return {'access_token': token, 'type': 'bearer'}


@auth_router.post('/default/token')
async def auth_default(
    credentials: LoginDTO, auth_service: AuthService = Depends(AuthService)
):
    token: str = await auth_service.login(credentials, LoginStrategies.DEFAULT)
    return {'access_token': token, 'type': 'bearer'}
