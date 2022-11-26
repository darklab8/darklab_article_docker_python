from fastapi import FastAPI

import src.example.views as example_views


def app_factory() -> FastAPI:
    from . import settings

    app = FastAPI()

    app.include_router(example_views.router)

    @app.get("/")
    def get_ping() -> dict[str, str]:
        return {"message": "pong!"}

    return app


if "main" in __name__:

    app = app_factory()