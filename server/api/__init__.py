from fastapi import FastAPI
from .routes import init_routes
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application services."""
    # Process Like Consumers and CronJobs
    yield
    # Finishing that Process


def create_app(default_lifespan = lifespan) -> FastAPI:
    """Creating FastAPI application."""
    app = FastAPI(title='Farm Stack Template', lifespan=default_lifespan)

    # Cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    init_routes(app)
    return app


app = create_app()
