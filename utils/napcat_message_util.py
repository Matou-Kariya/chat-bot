from datetime import datetime
from typing import Any

from entity.group_message import GroupMessage
from entity.group_message_attachment import GroupMessageAttachment


class NapcatMessageUtil:
    @staticmethod
    def to_group_message(raw_event: dict[str, Any]) -> GroupMessage:
        sender = raw_event.get("sender") or {}
        message_segments = raw_event.get("message") or []
        return GroupMessage(
            message_id=str(raw_event.get("message_id") or ""),
            group_id=str(raw_event.get("group_id") or ""),
            user_id=str(raw_event.get("user_id") or ""),
            nickname=NapcatMessageUtil._get_nickname(sender),
            message_text=NapcatMessageUtil._extract_text(message_segments),
            raw_message=str(raw_event.get("raw_message") or ""),
            raw_json=raw_event,
            message_time=NapcatMessageUtil._to_datetime(raw_event.get("time")),
        )

    @staticmethod
    def to_group_message_attachments(raw_event: dict[str, Any]) -> list[GroupMessageAttachment]:
        message_segments = raw_event.get("message") or []
        message_id = str(raw_event.get("message_id") or "")
        group_id = str(raw_event.get("group_id") or "")
        user_id = str(raw_event.get("user_id") or "")
        attachments: list[GroupMessageAttachment] = []
        for segment in message_segments:
            if not isinstance(segment, dict):
                continue
            segment_type = segment.get("type")
            data = segment.get("data") or {}
            if segment_type == "image":
                attachments.append(
                    NapcatMessageUtil._to_image_attachment(message_id=message_id, group_id=group_id, user_id=user_id,
                                                           data=data))
            elif segment_type == "record":
                attachments.append(
                    NapcatMessageUtil._to_record_attachment(message_id=message_id, group_id=group_id, user_id=user_id,
                                                            data=data))
        return attachments

    @staticmethod
    def _to_image_attachment(message_id: str, group_id: str, user_id: str,
                             data: dict[str, Any]) -> GroupMessageAttachment:
        summary = str(data.get("summary") or "")
        sub_type = NapcatMessageUtil._to_int(data.get("sub_type"))
        is_meme = (summary == "[动画表情]" or sub_type == 1)
        return GroupMessageAttachment(
            message_id=message_id,
            group_id=group_id,
            user_id=user_id,
            attachment_type="image",
            file_url=NapcatMessageUtil._to_optional_str(data.get("url")),
            local_path=None,
            is_meme=1 if is_meme else 0,
            text_content=None,
            summary=summary or None,
            tags={"file": data.get("file"), "file_size": NapcatMessageUtil._to_int(data.get("file_size")),
                  "sub_type": sub_type, "summary": summary, },
            perceptual_hash=None,
        )

    @staticmethod
    def _to_record_attachment(message_id: str, group_id: str, user_id: str,
                              data: dict[str, Any]) -> GroupMessageAttachment:
        return GroupMessageAttachment(
            message_id=message_id,
            group_id=group_id,
            user_id=user_id,
            attachment_type="record",
            file_url=NapcatMessageUtil._to_optional_str(data.get("url")),
            local_path=None,
            is_meme=0,
            text_content=None,
            summary=None,
            tags={
                "file": data.get("file"),
                "file_size": NapcatMessageUtil._to_int(data.get("file_size")),
                "source_path": data.get("path"),
            },
            perceptual_hash=None,
        )

    @staticmethod
    def _extract_text(message_segments: Any) -> str:
        if not isinstance(message_segments, list):
            return ""
        texts: list[str] = []
        for segment in message_segments:
            if not isinstance(segment, dict):
                continue
            if segment.get("type") != "text":
                continue
            data = segment.get("data") or {}
            text = str(data.get("text") or "").strip()
            if text:
                texts.append(text)
        return ",".join(texts).strip()

    @staticmethod
    def _get_nickname(sender: dict[str, Any]) -> str:
        return str(sender.get("card") or sender.get("nickname") or "")

    @staticmethod
    def _to_datetime(timestamp: Any) -> datetime | None:
        if timestamp is None or timestamp == "":
            return None
        return datetime.fromtimestamp(int(timestamp))

    @staticmethod
    def _to_optional_str(value: Any) -> str | None:
        if value is None or value == "":
            return None
        return str(value)

    @staticmethod
    def _to_int(value: Any) -> int | None:
        if value is None or value == "":
            return None
        return int(value)
