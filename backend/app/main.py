from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import settings 
from app.api.routers import api_router
from fastapi.staticfiles import StaticFiles
app= FastAPI(
    title=settings.project_name,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory="media"), name="media")
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.project_name}"}



app.include_router(api_router,prefix=settings.api_prefix)