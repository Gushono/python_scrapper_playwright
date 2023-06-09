from fastapi import FastAPI

from src.entrypoints.routers.router import add_routes


def create_app(debug_mode: bool) -> FastAPI:
    app = FastAPI()
    add_routes(app)

    if debug_mode:
        print(f"RUNNING ON DEBUG MODE, {debug_mode=}")
        app.debug = True

    return app
