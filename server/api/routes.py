from .user import user_router
from .auth import auth_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.config import settings


def init_routes(app: FastAPI):
    """Include All App Routes"""
    # Api Routes
    app.include_router(auth_router)
    app.include_router(user_router)

    # React APP
    templates = Jinja2Templates(directory=settings.REACT_BUILD_DIR)
    app.mount('/assets', StaticFiles(directory=settings.REACT_STATIC_FILES), 'assets')

    @app.get('/{path:path}', tags=['React App'])
    async def react_app(request: Request, path: str):
        """Redirect to react app if not exists in api"""
        return templates.TemplateResponse('index.html', {'request': request})
