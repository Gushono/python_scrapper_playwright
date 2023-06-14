import os

import uvicorn

from server import create_app

ENVIRONMENT = "development" if os.environ.get("PORT") is None else "production"
DEBUG = ENVIRONMENT == "development"

app = create_app(debug_mode=DEBUG)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
