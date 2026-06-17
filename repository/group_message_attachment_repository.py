from sqlalchemy.orm import Session

from entity.group_message_attachment import GroupMessageAttachment


class GroupMessageAttachmentRepository:
    # 数据库插入
    @staticmethod
    def save_all(db: Session, attachments: list[GroupMessageAttachment]) -> list[GroupMessageAttachment]:
        if not attachments:
            return []
        db.add_all(attachments)
        db.flush()
        return attachments
