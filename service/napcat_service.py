from repository.group_message_attachment_repository import GroupMessageAttachmentRepository
from repository.group_message_repository import GroupMessageRepository
from utils.napcat_message_util import NapcatMessageUtil
from sqlalchemy.orm import Session


class NapcatService:
    @staticmethod
    def save_message(event: dict, db: Session):
        if not NapcatMessageUtil.should_process(event):
            return
        group_message = NapcatMessageUtil.to_group_message(event)
        group_message_attachment = NapcatMessageUtil.to_group_message_attachments(event)
        try:
            GroupMessageRepository.save(db, group_message)
            GroupMessageAttachmentRepository.save_all(db, group_message_attachment)
            db.commit()
            print("消息入库成功...")
        except Exception:
            db.rollback()
            raise
