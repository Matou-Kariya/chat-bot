from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

from config.settings import settings


class LLMService:
    @staticmethod
    def deepseek():
        return ChatDeepSeek(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )

    @staticmethod
    def dashscope(model_type="chat"):
        model = settings.QWEN_CHAT_MODEL
        if model_type == "image":
            model = settings.QWEN_IMAGE_MODEL
        elif model_type == "voice":
            model = settings.QWEN_ASR_MODEL
        return ChatOpenAI(
            model=model,
            api_key=settings.DASHSCOPE_API_KEY,
            base_url=settings.QWEN_BASE_URL
        )
