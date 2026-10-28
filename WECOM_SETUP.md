# Sagt 企业微信配置要点（已排障验证）

项目路径（服务器 47.96.20.27）：`/home/workspace/sagt-202610/`

## 一、消息是怎么发出去的（参数链路）

```
sagt_client/.env  SAGT_USER_ID ──登录──▶ /sagt/get_token ──▶ USER_TOKEN
                        │                                        │
                        ▼                                        ▼
              thread 的 configurable.user_id            auth.py 校验 token
                        │                                        │
                        └──────────▶ wxwork_api.notify_user(touser=user_id, agentid=APP_ID)
                                                │
                                                ▼
                                    企业微信自建应用会话
```

| 参数 | 位置 | 作用 | 必须等于 |
|---|---|---|---|
| `WXWORK_CORP_ID` | sagt_agent/.env | 企业 ID | 自己企业的 CorpID |
| `WXWORK_APP_ID` | sagt_agent/.env | 自建应用 AgentId | 自己建的那个应用 |
| `WXWORK_APP_SECRET` | sagt_agent/.env | 应用 Secret | 同上 |
| `USER_ID` | sagt_agent/.env | **消息接收人**（企业微信成员 userid） | 通讯录里自己的账号 |
| `USER_EXTERNAL_ID` | sagt_agent/.env | 客户（外部联系人）ID，只用于 demo 数据与打标签 | 与客户端一致即可 |
| `USER_TOKEN` | sagt_agent/.env | 静态登录令牌，可自定义 | 无硬编码依赖，随便换 |
| `SAGT_USER_ID` | sagt_client/.env | 客户端登录账号 | **必须与 agent 的 USER_ID 完全一致** |
| `SAGT_USER_PASSWORD` | sagt_client/.env | 客户端登录密码 | 必须与 USER_PASSWORD 一致 |

## 二、这次踩到的三个坑

1. **客户端账号没跟着改**：agent 侧 `USER_ID=LiangShuo`，客户端还是教程的 `xiaocheng` → `/sagt/get_token` 直接 **403**，连 token 都拿不到，后续什么都不可能发出去。
2. **改完 `.env` 没重启服务**：`load_dotenv()` 在进程启动时读一次。服务 21:46 启动、`.env` 凌晨 01:00 才改 → 内存里仍是旧配置，消息全发到教程作者那边。**改完必须重启 `langgraph dev`**。
3. **找不到消息在哪**：自建应用的消息是发在「应用会话」里，不是普通聊天。去企业微信搜你建的应用名。

附带：`sagt_client/.env` 末尾曾残留一个孤立字符 `c`（中文引号导致命令未闭合留下的脏行），已清理。

## 三、当前生效配置（2026-10-28 验证通过）

- 企业微信成员：`LiangShuo`（姓名：梁硕）
- 登录：`/sagt/get_token` → 200，`USER_TOKEN` 已换成自生成的 `sagt_xxx`
- 推送：`WxWorkAPI().notify_user()` → True，手机端已收到验证消息
- 服务：`langgraph dev --port 2024`，日志 `/tmp/sagt_agent.log`

## 四、以后再出问题，按这三步自查（1 分钟定位）

```python
# 1. 拿 token：失败 = corp_id / secret 错
requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken",
             params={"corpid": CORP_ID, "corpsecret": SECRET})

# 2. 查成员：失败 = USER_ID 不是通讯录里的账号
requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/get",
             params={"access_token": TOKEN, "userid": USER_ID})

# 3. 发消息：失败 = agentid 错，或自己不在应用可见范围 / 服务器 IP 不在可信 IP
requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send",
              params={"access_token": TOKEN},
              json={"touser": USER_ID, "msgtype": "text",
                    "agentid": APP_ID, "text": {"content": "test"}})
```

常见 errcode：`60020` 可信 IP 未配置、`60011` 无权限/成员不在应用可见范围、`40056` 不合法的 agentid。

## 五、重启命令（注意别用 pkill 匹配启动脚本名，会把自己一起杀掉）

```bash
ps -eo pid,lstart,cmd | grep langgraph | grep -v grep   # 取 PID
kill -TERM <PID...>
cd /home/workspace/sagt-202610/sagt_agent && export PATH=/home/feifei/.local/bin:$PATH
setsid nohup ./run_sagt_agent_dev.sh > /tmp/sagt_agent.log 2>&1 &
```
