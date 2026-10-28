from models.sagt_models import CustomerTags, ChatHistory, KFChatHistory, OrderHistory, CustomerProfile
from llm.llm_setting import chat_model as llm
from langchain_core.messages import AIMessage
from utils.agent_logger import get_logger

logger = get_logger("llm_suggest_profile")

def llm_profile_suggest(chat_history: ChatHistory, kf_chat_history: KFChatHistory, order_history: OrderHistory, customer_tags: CustomerTags, customer_profile: CustomerProfile) -> CustomerProfile:

    prompt = _profile_instructions.format(
        chat_history=chat_history.model_dump_json(),
        kf_chat_history=kf_chat_history.model_dump_json(),
        order_history=order_history.model_dump_json(),
        customer_tags=customer_tags.model_dump_json(),
        customer_profile=customer_profile.model_dump_json(),
        schema_json=CustomerProfile.get_schema_json(),
        example_json=CustomerProfile.get_example_json(),
    )

    logger.debug(f"prompt: {prompt}")

    # 生成客户profile建议
    generated_result: AIMessage = llm.invoke(prompt)
    logger.debug(f"generated_result: {generated_result}")

    if generated_result and generated_result.content:
        generated_profile_json = generated_result.content
    else:
        generated_profile_json = "{}"

    try:
        generated_profile = CustomerProfile.model_validate_json(generated_profile_json)
        logger.info(f"generated_profile: {generated_profile.model_dump_json()}")
        return generated_profile
    except Exception as e:
        logger.error(f"生成客户profile建议失败: {e}")
        return CustomerProfile()



_profile_instructions = """
你的任务是根据客户的相关信息，提取客户的profile信息：CustomerProfile。

这里是客户profile信息CustomerProfile的数据结构定义：
-------------------
{schema_json}
-------------------

json对象示例：
-------------------
{example_json}
-------------------


请根据下面的客户信息，生成CustomerProfile：

1、【重要】您必须回复一个有效JSON对象。
2、请不要在JSON对象前后包含任何文本。也不要包含“```json”或者“```”这样的文本。
3、JSON对象结构必须符合CustomerProfile的定义
4、内容包含你认为可以描述客户情况的所有信息。
5、旧profile中需要保留的信息，也更新到新的profile中，业务系统使用新profile时，会完整覆盖旧的profile。



示例目标字段：

1. 【姓名】:包括昵称、曾用名等可能相关的称呼。
2. 【年龄】: 精确到具体岁数，若提及大概年龄段也需注明。
3. 【性别】: 明确是男、女或其他表述。
4. 【职业】: 具体的工作类型，如包含多个职业可全部列出。
5. 【兴趣爱好】: 如具体的运动项目、音乐类型等。
6. 【婚姻状况】: 是否已婚、未婚、离异等。
7. 【教育程度】: 如高中、本科、硕士等。
8. 【住房情况】: 如户型、面积、装修状态、自住或出租等。
9. 【装修需求】: 如全屋定制、局部改造、风格偏好（原木、极简、新中式等）。
10. 【装修预算】: 如总预算42万、可接受浮动区间等。
11. 【工期要求】: 如希望孩子开学前入住、可接受工期天数等。
12. 【关注重点】: 如环保等级、收纳量、五金品牌、施工噪音控制等。
13. 【决策链】: 如本人决策、爱人共同决策、父母参与意见等。
14. 【出行方式】: 如自驾、公交、地铁等。
15. 【宠物情况】: 是否养宠物及宠物种类。
16. 【娱乐活动偏好】: 如看电影、唱K等具体活动。
17. 【家庭成员】: 如配偶、子女等。
18. 【已购产品与服务】: 如柜体、厨房家电包、软装包、延保服务等。
19. 【品牌偏好与竞品对比】: 如对比过索菲亚、欧派等品牌及关注点。
20. 【消费频率】: 如每周一次、每月几次等。
21. 【消费场景】: 如自住改善、出租配置、子女婚房等。
22. 【每次消费的大致金额】: 如100元。
23. 【售后敏感度】: 如对延期赔付、增项透明、保修年限的关注。
24. 【购买渠道】: 如线下实体店、线上电商平台等。

下面是客户的数据：



这里是客户和销售人员近期的对话记录：
-------------------
{chat_history}
-------------------

这里是客户和客服近期的对话记录：
-------------------
{kf_chat_history}
-------------------

这里是客户近期的订单信息：
-------------------
{order_history}
-------------------

这里是客户的标签信息：
-------------------
{customer_tags}
-------------------

这里是客户之前的profile信息：
-------------------
{customer_profile}
-------------------

"""
