from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import src.example.views as example_views


def app_factory() -> FastAPI:
    from . import settings

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(example_views.router)

    @app.get("/")
    def get_ping() -> dict[str, str]:
        return {"message": "pong!"}

    return app


if "main" in __name__:

    app = app_factory()