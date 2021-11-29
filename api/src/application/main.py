import uvicorn
from fastapi import FastAPI

from application.infrastructure.database.database import create_database
from application.rest_api.app_factory import create_housing_units_app

app: FastAPI = create_housing_units_app(name="Housing Units API")


@app.on_event("startup")
async def on_startup():
    # Initialize the tables if not exist.
    await create_database()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
