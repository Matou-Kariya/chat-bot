from sqlalchemy import select
from sqlalchemy.orm import Session

from entity.group_message import GroupMessage


class GroupMessageRepository:
    # 数据库插入
    @staticmethod
    def save(db: Session, message: GroupMessage) -> GroupMessage:
        db.add(message)
        db.flush()
        db.refresh(message)
        return message

    # 根据id查消息
    @staticmethod
    def get_by_message_id(db: Session, message_id: str) -> GroupMessage | None:
        stmt = select(GroupMessage).where(GroupMessage.message_id == message_id)
        return db.execute(stmt).scalar_one_or_none()
