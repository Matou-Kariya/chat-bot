from fastapi import APIRouter, Depends
from fastapi import Request
from sqlalchemy.orm import Session

from service.napcat_service import NapcatService
from utils.database import get_db

router = APIRouter()


@router.post("/message")
async def receive_event(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print(f"收到napcat消息:{body}")
    NapcatService.save_message(body, db)
    return {
        "status": "ok"
    }
