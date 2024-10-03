import decouple as env
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_NAME: str = env.config('DATABASE_NAME')
    DATABASE_URI: str = env.config('DATABASE_URI')
    SHOW_SQL: bool = env.config('SHOW_SQL')

    # Jwt
    ALGORITHM: str = 'HS256'
    TOKEN_SECRET: str = env.config('TOKEN_SECRET')
    EXPIRATION_SECONDS: int = 60 * 60 * 5  # 5 Hours

    # Google OAuth2
    GOOGLE_CLIENT_ID: str = env.config('GOOGLE_CLIENT_ID')
    GOOGLE_REDIRECT_URI: str = env.config('GOOGLE_REDIRECT_URI')
    GOOGLE_CLIENT_SECRET: str = env.config('GOOGLE_CLIENT_SECRET')

    # Frontend Dir
    REACT_BUILD_DIR: str = env.config('REACT_BUILD_DIR')
    REACT_STATIC_FILES: str = f'{REACT_BUILD_DIR}/assets'


settings = Settings()
