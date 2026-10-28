# 演示业务场景说明

本项目原教程内置的业务场景为「酒类销售」（客户程哥 / 茅台），已整体改造为
**木言整装 · 高端全屋定制** 场景，便于演示销售助手的完整能力。

## 角色设定

| 角色 | 说明 |
|---|---|
| 销售人员（销冠） | 梁硕，`user_id = LiangShuo` |
| 客户 | 陈曼（陈姐），改善型住房业主，三居改四居 |

## 客户关键背景

- 预算 42 万，爱人参与把关；关注环保（母亲有鼻炎）、收纳量、工期
- 家庭成员：爱人、女儿（补课）、母亲（计划来住两个月）
- 养猫，猫会抓沙发和柜门板
- 对比过欧派、索菲亚，最终因 ENF 级板材 + 百隆五金 + 十年质保选择我方
- 对延期赔付、增项透明度、保修年限高度敏感；已产生一次转介绍

## 改造涉及的文件

| 文件 | 改动 |
|---|---|
| `store_client/sagt_demo_init.py` | 员工/客户、26 条企微聊天、30 条客服记录、8 条合同订单、14 个标签 |
| `src/llm/llm_suggest_chat.py` | 销售助理人设：酒类 → 全屋定制（整装） |
| `src/llm/llm_suggest_profile.py` | 24 个画像字段模板改为家装场景 |
| `src/models/sagt_models.py` | 客户画像示例 schema 改为家装业务 |
| `src/tools/store_tool.py` | 替换硬编码注入的两条演示消息（用于触发日程子图） |

> 注意：`get_chat_history()` 会固定追加两条消息，其中「明天上午10点 + 上门」是
> 触发**日程子图**的关键结构，修改时不要破坏这个模式。

## 重新初始化数据

演示数据存放在 LangGraph Store 中，`langgraph dev` 为内存模式，
**服务重启后数据会丢失，需要重新初始化**：

```bash
cd sagt_client
uv run python store_client/sagt_demo_init.py
```

更换业务场景时，需先清理旧数据再初始化（`upsert` 不会覆盖，会新旧混杂）：

```bash
uv run python store_client/sagt_store_test.py   # 使用 test_cleanup 按 namespace 清理
```

## 可演示的链路

- `profile_suggestion`：生成客户画像 → 企微通知 → 人工确认后写回
- `tag_suggestion`：基于聊天与订单推荐客户标签
- `schedule_suggestion`：识别「明天上午10点上门复尺」并创建企微日程
- `chat_suggestion` / `kf_chat_suggestion`：聊天与客服回复建议
