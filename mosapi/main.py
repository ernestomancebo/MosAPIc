from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from mosapi.routes import all_routes
from mosapi.settings import get_settings

app = FastAPI()

# Middlewares
# TODO: do an iteration for middlewares.
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[
                   get_settings().APP_TRUSTED_HOSTS])
# app.add_middleware(ProcessTimeHeaderMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=get_settings().APP_ALLOWED_HOSTS,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

# Routers
for router in all_routes:
    app.include_router(router.router)


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.get("/")
async def root():
    return {"message": "Hi there!"}
