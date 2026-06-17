from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Text, JSON, DateTime

from utils.database import Base


class GroupMessage(Base):
    __tablename__ = "group_message"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(String(64))
    group_id = Column(String(64))
    user_id = Column(String(64))
    nickname = Column(String(128))
    message_text = Column(Text)
    raw_message = Column(Text)
    raw_json = Column(JSON)
    message_time = Column(DateTime)
    created_at = Column(
        DateTime,
        default=datetime.now
    )

    def __repr__(self):
        return (
            f"GroupMessage("
            f"message_id={self.message_id!r}, "
            f"group_id={self.group_id!r}, "
            f"user_id={self.user_id!r}, "
            f"nickname={self.nickname!r}, "
            f"message_text={self.message_text!r}"
            f")"
        )