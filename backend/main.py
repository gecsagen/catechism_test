import logging
import uvicorn
from fastapi import FastAPI

from user.api import user_router
from user.api_login import login_router


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI(debug=True)
    application.include_router(user_router, prefix="/api/users", tags=["user"])
    application.include_router(login_router, prefix="/login", tags=["login"])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


@app.get("/api/healthchecker")
async def root():
    return {"message": "The API is LIVE!!"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)