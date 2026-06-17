from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Text, JSON, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from utils.database import Base


class GroupMessageAttachment(Base):
    __tablename__ = "group_message_attachment"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(String(64))
    group_id = Column(String(64))
    user_id = Column(String(64))
    attachment_type = Column(String(32))
    file_url = Column(Text)
    local_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_meme = Column(Integer)
    text_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags = Column(JSON)
    perceptual_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at = Column(
        DateTime,
        default=datetime.now
    )

    def __repr__(self):
        return (
            f"GroupMessageAttachment("
            f"message_id={self.message_id!r}, "
            f"attachment_type={self.attachment_type!r}, "
            f"file_url={self.file_url!r}, "
            f"is_meme={self.is_meme!r}, "
            f"summary={self.summary!r}"
            f")"
        )
