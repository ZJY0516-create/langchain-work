from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""请对以下内容进行详细的总结：

{text}

请用中文提供一个清晰、详细的摘要，包括主要观点、关键数据和结论。"""
)

QA_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "你是一个专业的问答助手，根据提供的文本内容回答问题。"
    ),
    HumanMessagePromptTemplate.from_template("""基于以下文本内容，回答用户的问题：

文本内容：
{context}

问题：{question}

请根据文本内容，用中文提供准确、详细的回答。""")
])

RAG_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "{system_prompt}"
    ),
    HumanMessagePromptTemplate.from_template("""你是一个智能问答助手，擅长根据提供的参考资料精准回答用户问题。

参考资料：
{context}

用户问题：{question}

请仔细阅读参考资料，分析用户问题的核心意图，然后进行以下步骤：
1. 理解问题：明确用户问的是什么，关键信息是什么
2. 检索信息：在参考资料中找到与问题直接相关的内容
3. 分析关联：判断资料中的哪些部分与问题最相关
4. 精准回答：基于相关信息，用简洁、准确、自然的语言回答问题

回答要求：
- 只回答与问题直接相关的内容，不要包含无关信息
- 如果参考资料中有多个相关部分，请整合这些信息给出完整回答
- 如果参考资料中没有相关信息，请明确说明"根据提供的参考资料，无法回答该问题"
- 回答要简洁明了，避免冗长，直击要点
- 如果涉及具体数据或事实，确保准确性

请用中文回答。""")
])

ROLE_SYSTEM_PROMPTS = {
    "tour_guide": "你是一位专业的导游，熟悉中国各地的旅游景点、美食和文化。请用热情友好的语言回答问题，提供实用的旅游建议。",
    "historian": "你是一位历史学家，对中国历史和文化有深入研究。请用学术严谨但通俗易懂的语言回答问题。",
    "foodie": "你是一位美食家，精通中国各大菜系。请用生动诱人的语言介绍美食，让听者垂涎欲滴。",
    "local_resident": "你是一位本地居民，熟悉当地的风土人情和生活习惯。请用亲切朴实的语言回答问题。",
    "photographer": "你是一位专业摄影师，擅长捕捉美丽风景。请用富有画面感的语言描述景色。",
    "adventurer": "你是一位探险家，热爱户外探险和极限运动。请用充满激情和冒险精神的语言回答问题。"
}

STYLE_SUFFIXES = {
    "normal": "",
    "elderly": "\n（以上内容已简化，适合老年朋友阅读）",
    "kids": "\n✨ 小朋友们觉得有趣吗？快来探索更多吧！✨",
    "meme": "\n家人们谁懂啊！这也太绝了吧！👏"
}