import logging

from fastapi import FastAPI

from user.api import user_router


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(user_router, prefix="/api/users", tags=["user"])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}
