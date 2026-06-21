# 消息路由，分发不同的消息
from utils.napcat_message_util import NapcatMessageUtil


class MessageRouter:
    RouterType = [
        'REPEAT',  # 复读
        'CHAIN',  # 接龙
        'AUTONOMOUS',  # 自主回复
        'COMMAND'  # 命令类型
    ]

    @staticmethod
    def handle(raw_event: dict):
        if NapcatMessageUtil.is_at_bot(raw_event):
            # 有人艾特机器人
            pass
        else:
            pass

    # 用于路由常规非艾特的消息
    @staticmethod
    def _router(raw_event: dict):
        pass
