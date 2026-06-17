from fastapi import FastAPI
from napcat.napcat_event import router as napcat_router
app = FastAPI(title="Chat Bot")


app.include_router(napcat_router, prefix="/napcat", tags=["NapCat"])
