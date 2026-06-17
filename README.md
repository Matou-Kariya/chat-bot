第一阶段：核心消息管线
1. 重构 NapCat 事件解析
2. 统一消息对象 MessageEvent
3. 完成消息入库、附件入库
4. 完成机器人自身消息过滤
5. 完成群状态记录和冷却逻辑

第二阶段：回复路由
6. 建 ChatRouter
7. 明确功能优先级
8. @ 回复接入新路由
9. 自主回复接入新路由
10. 修复 TopicService 和 CharacterService 数据结构不一致

第三阶段：记忆系统
11. 建群画像、群友画像、群记忆表
12. 先支持手写 Markdown 画像加载
13. 回复 prompt 接入用户画像和群记忆
14. 再做每日画像提炼任务

第四阶段：剑网三知识库/工具调用
15. 建本地攻略知识库
16. 建 KnowledgeRouter
17. 支持本地知识检索
18. 再接 web search 工具
19. 工具结果二次交给大模型生成最终回复

第五阶段：媒体能力
20. 图片/语音附件下载
21. 图片 OCR/视觉理解
22. 语音 ASR
23. 表情包去重、统计、复用

第六阶段：娱乐功能
24. 复读
25. 诗词/歌词接龙
26. TTS
27. 唱一句

第七阶段：数据生命周期
28. 原始消息清理
29. 附件清理
30. 向量库 upsert/删除
31. 管理命令和后台维护脚本

LBL_ChatBot/
  main.py

  api/
    napcat_event_api.py

  core/
    config.py
    logger.py
    exceptions.py
    constants.py

  config/
    database_config.py
    global_config.py
    llm_config.py
    napcat_config.py
    feature_flags.py

  model/
    message.py
    attachment.py
    group_state.py
    memory.py
    media.py
    knowledge.py
    entertainment.py

  repository/
    base_repository.py
    message_repository.py
    attachment_repository.py
    group_state_repository.py
    memory_repository.py
    media_repository.py
    knowledge_repository.py

  service/
    message/
      event_parser.py
      message_ingest_service.py
      message_context_service.py

    router/
      chat_router.py
      route_result.py

    reply/
      mention_reply_service.py
      autonomous_reply_service.py
      final_reply_service.py
      prompt_builder.py

    intent/
      intent_service.py
      topic_service.py
      knowledge_router_service.py

    memory/
      profile_service.py
      group_memory_service.py
      retrieval_service.py
      profile_refresh_service.py

    knowledge/
      jx3_knowledge_service.py
      local_knowledge_loader.py
      web_search_service.py
      web_page_fetch_service.py

    media/
      attachment_analysis_service.py
      image_understanding_service.py
      audio_transcription_service.py
      meme_asset_service.py
      perceptual_hash_service.py

    entertainment/
      entertainment_router.py
      echo_service.py
      chain_service.py
      voice_command_service.py

    tool/
      tool_registry.py
      tool_types.py

    napcat/
      napcat_message_service.py

    llm/
      model_service.py
      ai_client_factory.py

  job/
    scheduler.py
    idle_reply_job.py
    chicken_soup_job.py
    profile_refresh_job.py
    media_analysis_job.py
    data_retention_job.py

  knowledge/
    group/
      group_profile.md
      members/
        123456.md
    jx3/
      pvp/
      pve/
      faq/
    chain/
      poems.json
      meme_lines.json

  prompt/
    character_prompt.py
    intent_prompt.py
    topic_prompt.py
    knowledge_prompt.py
    media_prompt.py

  scripts/
    init_db.py
    rebuild_db.py
    import_profiles.py
    reindex_vector_store.py

  tests/
    test_event_parser.py
    test_router.py
    test_prompt_builder.py
  

MessageEventParser
把 NapCat 原始 event 转成统一 MessageEvent，后面所有 service 都不直接碰原始 dict。

MessageIngestService
负责保存文本消息、附件消息、raw_json。

MessageContextService
负责整理最近聊天上下文、最近媒体上下文、当前用户上下文。

ChatRouter
总路由。判断一条消息应该走命令、@回复、知识问答、娱乐、自主回复还是不回复。

MentionReplyService
处理 @ 机器人消息，走完整 RAG/工具链。

AutonomousReplyService
处理普通消息的低频自主回复，只拿轻量上下文。

FinalReplyService
最终回复生成器。接收画像、记忆、知识、媒体、工具结果，拼 prompt 调模型。

PromptBuilder
统一拼 prompt，避免 prompt 散落在各个 service 里。

IntentService
判断用户意图：求助、攻略、吐槽、攻击、玩梗、命令等。

TopicService
判断话题：剑网三、男女对立、地域、键政、日常、其他游戏等。

KnowledgeRouterService
判断是否需要攻略知识、是否需要最新资料、是否需要 web search。

ProfileService
读取/更新群友画像。

GroupMemoryService
管理群梗、群事件、关系、长期记忆。

RetrievalService
统一做 RAG 检索：用户画像、群记忆、攻略知识、表情包语义。

Jx3KnowledgeService
检索本地剑网三攻略知识库。

WebSearchService
执行互联网搜索，返回带来源、时间、正文摘要的结果。

ToolRegistry
统一注册和调用工具，比如 web_search、jx3_knowledge、image_understanding、tts。

AttachmentAnalysisService
调度图片/语音分析。

ImageUnderstandingService
OCR、多模态图片理解、表情包语义识别。

AudioTranscriptionService
ASR 语音转文字。

MemeAssetService
表情包去重、统计、热门表情包选择。

EntertainmentRouter
娱乐功能路由。

EchoService
复读。

ChainService
诗词/歌词/群梗接龙。

VoiceCommandService
TTS 和唱一句命令。

DataRetentionJob
定期清理原始消息、图片、语音和过期向量数据。