"""
SAGT 演示数据初始化脚本

业务场景：木言整装 · 高端全屋定制
销冠（员工）：梁硕   user_id = LiangShuo
客户：陈曼（陈姐）   改善型住房业主，三居改四居

用于初始化企业标签、员工客户信息、聊天记录和订单数据的演示脚本。
"""

import logging
from datetime import datetime
from sagt_store_api import create_sagt_store_api
import sys
import os
from dotenv import load_dotenv

load_dotenv()


from datetime_string import datetime2timestamp

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

## 测试用的客户ID
SAGT_EXTERNAL_ID = os.getenv("SAGT_EXTERNAL_ID")

## sagt账号信息
SAGT_USER_ID = os.getenv("SAGT_USER_ID")
SAGT_USER_PASSWORD = os.getenv("SAGT_USER_PASSWORD")
SAGT_SERVER_URL = os.getenv("SAGT_SERVER_URL")


class DemoDataInitializer:
    """演示数据初始化器"""
    
    store_client = None

    def __init__(self, server_url: str, user_id: str, password: str):
        self.store_client = create_sagt_store_api(server_url, user_id, password)
        
    def init_all_data(self):
        """初始化所有演示数据"""
        logger.info("开始初始化演示数据...")
        
        try:
            # 1. 初始化标签
            self.init_tags() # 注意标签ID和企业微信中的不一致。测试期间可以使用。
            
            # 2. 初始化用户信息
            self.init_user_and_customer()
            
            # 3. 初始化聊天记录
            self.init_wxqy_messages()

            # 4. 初始化聊天记录
            self.init_wxkf_messages()
            
            # 5. 初始化订单记录
            self.init_orders()
            
            logger.info("演示数据初始化完成！")
            
        except Exception as e:
            logger.error(f"初始化演示数据失败: {e}")
            raise

    def init_tags(self):
        """初始化企业标签"""
        logger.info("正在初始化企业标签...")
        

        # {"tag_id": "tag_004","tag_name": "商务合作","strategy_id": 2,"group_id": "service_type","group_name": "服务类型","deleted": False}

        # 基础属性标签
        basic_tags = [
            {"tag_id": "stE8gRKQAA-dAKMiJZw1MP4s_drOAh2Q", "tag_name": "高净值客户",   "group_id": "stE8gRKQAA4U6yUFhEhAXQ1BHZ5jt0_Q", "group_name": "基础属性", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAA7TJ7kvuKMeAA7FmcDY8Wg", "tag_name": "中年女性",     "group_id": "stE8gRKQAA4U6yUFhEhAXQ1BHZ5jt0_Q", "group_name": "基础属性", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAdN5SvmZoNc5n6Up12dPp-A", "tag_name": "已婚有子女",   "group_id": "stE8gRKQAA4U6yUFhEhAXQ1BHZ5jt0_Q", "group_name": "基础属性", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAJvszKCI8cCQJ0paQP2u9Wg", "tag_name": "家有老人",     "group_id": "stE8gRKQAA4U6yUFhEhAXQ1BHZ5jt0_Q", "group_name": "基础属性", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAJvszKCI8cCQJ0paQP2u9W1", "tag_name": "养宠家庭",     "group_id": "stE8gRKQAA4U6yUFhEhAXQ1BHZ5jt0_Q", "group_name": "基础属性", "strategy_id": 2, "deleted": False},
        ]
        
        # 消费行为标签
        buy_tags = [
            {"tag_id": "stE8gRKQAA3EbL1cO0YS0cyupiATvFqA", "tag_name": "整装全屋定制", "group_id": "stE8gRKQAAdkLtKRp5u1HBHTYaGDbHhA", "group_name": "消费行为", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAhRYl-8b_Z2hzcimwynFIEA", "tag_name": "环保板材偏好", "group_id": "stE8gRKQAAdkLtKRp5u1HBHTYaGDbHhA", "group_name": "消费行为", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAASj3DlY9G97EkhUBZmlwgrg", "tag_name": "智能家居配套", "group_id": "stE8gRKQAAdkLtKRp5u1HBHTYaGDbHhA", "group_name": "消费行为", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAEJGWP7O1vHTDZn4ep0fWxQ", "tag_name": "软装家电连带", "group_id": "stE8gRKQAAdkLtKRp5u1HBHTYaGDbHhA", "group_name": "消费行为", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAo-zv5-_oEWt__adANrQK1Q", "tag_name": "高客单增项",   "group_id": "stE8gRKQAAdkLtKRp5u1HBHTYaGDbHhA", "group_name": "消费行为", "strategy_id": 2, "deleted": False},
        ]
        
        # 社交关系标签
        social_tags = [
            {"tag_id": "stE8gRKQAAkgEe-7wvit1OPLqaUV55Hg", "tag_name": "转介绍意愿强", "group_id": "stE8gRKQAA3IKjjLIzWF7sZ1gy8UJzYQ", "group_name": "社交关系", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAA4yE1-7IkO8SzvIOsCQej9A", "tag_name": "邻里口碑传播", "group_id": "stE8gRKQAA3IKjjLIzWF7sZ1gy8UJzYQ", "group_name": "社交关系", "strategy_id": 2, "deleted": False},
        ]
        
        # 服务敏感度标签
        service_tags = [
            {"tag_id": "stE8gRKQAAT4k2ZHMxooZjfORj-AdH4A", "tag_name": "工期敏感",         "group_id": "stE8gRKQAAYywcJoxIOzqvDLm5XSXi_g", "group_name": "服务敏感度", "strategy_id": 2, "deleted": False},
            {"tag_id": "stE8gRKQAAzZCHpp3W4sDwt1vO_EQyVQ", "tag_name": "依赖设计师1v1服务", "group_id": "stE8gRKQAAYywcJoxIOzqvDLm5XSXi_g", "group_name": "服务敏感度", "strategy_id": 2, "deleted": False},
        ]
        
        
        # 合并所有标签
        all_tags = basic_tags + buy_tags + social_tags + service_tags
        
        # 批量创建标签
        for tag in all_tags:
            try:
                self.store_client.upsert_tags_setting(
                    tag_id=tag["tag_id"],
                    tag_name=tag["tag_name"],
                    group_id=tag["group_id"],
                    group_name=tag["group_name"],
                    strategy_id=tag["strategy_id"],
                    deleted=tag["deleted"]
                )
                logger.info(f"创建标签: {tag['tag_id']} - {tag['tag_name']}")
            except Exception as e:
                logger.warning(f"标签 {tag['tag_id']} 可能已存在: {e}")
        
        logger.info(f"标签初始化完成，共处理 {len(all_tags)} 个标签")
    
    def init_user_and_customer(self):
        """初始化员工和客户信息"""
        logger.info("正在初始化用户信息...")
        
        # 1. 创建员工信息
        employee_data = {
            "user_id": SAGT_USER_ID,
            "name": "梁硕",
        }
        
        try:
            self.store_client.upsert_employee(
                user_id=employee_data["user_id"],
                name=employee_data["name"]
            )
            logger.info(f"创建员工: {employee_data['user_id']} - {employee_data['name']}")
        except Exception as e:
            logger.warning(f"员工 {employee_data['user_id']} 可能已存在: {e}")
        
        # 2. 创建客户信息
        customer_data = {
            "external_id": SAGT_EXTERNAL_ID,
            "name": "陈曼",
            "remark_name": "陈姐",
            "union_id": "union001",
            "follow_user_id": SAGT_USER_ID,
            "tags": ["etE8gRKQAANeNZh8ttsqCe-S-XIEsPdQ", "etE8gRKQAA6xbQIT5mE62_WSKeiWVbAg", "etE8gRKQAAdm3IQ7SVSEtb5BrRzQJHnQ"]
        }
        
        try:
            self.store_client.upsert_external_user(
                external_id=customer_data["external_id"],
                union_id=customer_data["union_id"],
                follow_user_id=customer_data["follow_user_id"],
                name = customer_data["name"],
                remark_name = customer_data["remark_name"],
                tags = customer_data["tags"],
            )
            logger.info(f"创建客户: {customer_data['external_id']} - {customer_data['name']}")
        except Exception as e:
            logger.warning(f"客户 {customer_data['external_id']} 可能已存在: {e}")
        
        logger.info("员工和客户信息初始化完成")
    
    def init_wxqy_messages(self):
        """初始化企业微信聊天记录"""
        logger.info("正在初始化企业微信聊天记录...")
        
        # {"msg_id": "wxqy_002", "from_id": "ext_001", "to_id": "emp_001", "content": "请问贵公司的技术方案有哪些优势？", "msg_time": 3000, "seq": 2}

        # 企业微信聊天记录
        wxqy_messages = [
            # 量房后方案沟通
            {"seq": 1, "msg_id": "wxqy_001", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-09-22 09:15:00"), "content": "陈姐，昨天量房的数据我整理好了，三居改四居的方案今晚发您，先给您看个同户型的落地效果。"},
            {"seq": 2, "msg_id": "wxqy_002", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2025-09-22 09:20:00"), "content": "好啊，我最关心的是收纳，家里东西实在太多了。"},
            {"seq": 3, "msg_id": "wxqy_003", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-09-22 09:22:00"), "content": "明白，我按顶天立地柜+榻榻米+玄关组合给您排，储物量能多出四成左右。"},

            # 邀约看样板间
            {"seq": 4, "msg_id": "wxqy_004", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-10-08 11:05:00"), "content": "陈姐，国庆这两天样板间开放，盐系原木那套就是您说的风格，要不要实地看看？"},
            {"seq": 5, "msg_id": "wxqy_005", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2025-10-08 11:15:00"), "content": "想去！不过我女儿补课，只有周末上午有空。"},
            {"seq": 6, "msg_id": "wxqy_006", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-10-08 11:20:00"), "content": "那约周六上午十点，我让设计师一起在，现场给您改方案。"},

            # 宠物与板材细节
            {"seq": 7, "msg_id": "wxqy_007", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2025-10-09 10:20:00"), "content": "对了，我家猫特别爱抓沙发，你们板材耐不耐抓？"},
            {"seq": 8, "msg_id": "wxqy_008", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-10-09 10:25:00"), "content": "客厅和主卧建议用实木贴皮+耐磨烤漆，猫抓不留痕，我给您加了隐形防抓条。"},

            # 竞品比价
            {"seq": 9, "msg_id": "wxqy_009", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2025-11-03 14:05:00"), "content": "我对比了索菲亚和欧派，你们贵了快四万，凭什么？"},
            {"seq": 10, "msg_id": "wxqy_010", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-11-03 14:10:00"), "content": "姐，差价主要在五金和环保等级：我们是ENF级爱格板+百隆阻尼铰链，质保十年，他们多是E0级颗粒板。"},
            {"seq": 11, "msg_id": "wxqy_011", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2025-11-03 14:30:00"), "content": "环保这点我信你，我妈有鼻炎，甲醛这块不能有闪失。"},
            {"seq": 12, "msg_id": "wxqy_012", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2025-11-03 14:35:00"), "content": "放心，完工后我给您安排第三方CMA甲醛检测，不合格我们全额整改。"},

            # 增项顾虑
            {"seq": 13, "msg_id": "wxqy_013", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-01-07 10:12:00"), "content": "[转发文章《装修增项的十个坑》] 小梁你看看，我不会也被增项吧？"},
            {"seq": 14, "msg_id": "wxqy_014", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-01-07 10:20:00"), "content": "姐，我们是闭口合同，柜体之外的任何增项都要您签字才生效，我把它写进合同附件。"},

            # 签单与预算拉锯
            {"seq": 15, "msg_id": "wxqy_015", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-01-12 09:30:00"), "content": "姐，年底工厂要放假，这周签单能赶上年前排产，开春就安装，孩子开学前能住进去。"},
            {"seq": 16, "msg_id": "wxqy_016", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-01-12 09:33:00"), "content": "行，这周我去店里。不过预算我爱人卡在42万，超了要念我。"},
            {"seq": 17, "msg_id": "wxqy_017", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-01-12 09:40:00"), "content": "我给您做了41.8万的版本，主卧衣柜按原方案，次卧降到平板门，差价我做成老客户优惠单。"},

            # 开工与工期
            {"seq": 18, "msg_id": "wxqy_018", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-03-02 15:10:00"), "content": "合同签了，什么时候能开工？"},
            {"seq": 19, "msg_id": "wxqy_019", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-03-02 15:15:00"), "content": "下周进场拆除，工期65天，我拉个专属群，每天给您发进度照片。"},
            {"seq": 20, "msg_id": "wxqy_020", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-03-28 09:40:00"), "content": "邻居说装修噪音大，我怕被投诉。"},
            {"seq": 21, "msg_id": "wxqy_021", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-03-28 09:45:00"), "content": "我们已办装修备案，施工只在工作日9-12点、14-18点，周末静音施工，物业那边我提前打招呼。"},

            # 安装验收与售后
            {"seq": 22, "msg_id": "wxqy_022", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-04-15 16:20:00"), "content": "柜体装好了，效果真不错！就是主卧柜门有点异响。"},
            {"seq": 23, "msg_id": "wxqy_023", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-04-15 16:25:00"), "content": "明天让安装师傅上门调铰链，顺带给全屋柜体做一次免费保养。"},

            # 转介绍
            {"seq": 24, "msg_id": "wxqy_024", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-19 10:05:00"), "content": "我同事最近也要装修，能介绍给你吗？"},
            {"seq": 25, "msg_id": "wxqy_025", "from_id": SAGT_USER_ID, "to_id": SAGT_EXTERNAL_ID, "msg_time": datetime2timestamp("2026-06-19 10:10:00"), "content": "太感谢姐了！她签单我给您申请5000元答谢金，或者等价的全屋深度保洁套餐。"},

            # 二次需求
            {"seq": 26, "msg_id": "wxqy_026", "from_id": SAGT_EXTERNAL_ID, "to_id": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-08-03 11:00:00"), "content": "下个月我妈来住两个月，次卧那块还能加个扶手吗？"},
        ]
        
        # 批量创建企业微信消息
        for msg in wxqy_messages:
            try:
                self.store_client.upsert_wxqy_msg(
                    msg_id=msg["msg_id"],
                    from_id=msg["from_id"],
                    to_id=msg["to_id"],
                    content=msg["content"],
                    msg_time=msg["msg_time"],
                    seq=msg["seq"]
                )
                logger.info(f"创建企业微信消息: {msg['msg_id']}")
            except Exception as e:
                logger.warning(f"企业微信消息 {msg['msg_id']} 可能已存在: {e}")
        
        logger.info(f"企业微信聊天记录初始化完成，共处理 {len(wxqy_messages)} 条消息")

    def init_wxkf_messages(self):
        """初始化微信客服聊天记录"""
        logger.info("正在初始化微信客服聊天记录...")
        
        # {"msg_id": "msg_kf_001", "external_id": "dacheng001", "open_kfid": "kf001", "servicer_userid": "xiaozhang", "msg_time": 600, "origin": 5, msgtype": "text", "content": "关于定制化方案的详细信息，我已经发送到您的邮箱"}
        # 微信客服聊天记录
        wxkf_messages = [
            # 柜门异响
            {"msg_id": "msg_kf_001", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-01 09:05:00"), "origin": 3, "msgtype": "text", "content": "柜门异响都两周了，还没解决。"},
            {"msg_id": "msg_kf_002", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-01 09:10:00"), "origin": 5, "msgtype": "text", "content": "陈女士您好，已加急派单，师傅明天10点上门，这次直接为您更换一组新阻尼铰链~"},

            # 台面发霉
            {"msg_id": "msg_kf_003", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-01 14:20:00"), "origin": 3, "msgtype": "text", "content": "厨房台面接缝处发黑，是不是渗水了？"},
            {"msg_id": "msg_kf_004", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-01 14:25:00"), "origin": 5, "msgtype": "text", "content": "已登记，师傅上门会带防霉胶重做密封，并做48小时闭水测试~"},

            # 智能设备配网
            {"msg_id": "msg_kf_005", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-02 11:00:00"), "origin": 3, "msgtype": "text", "content": "你们的智能灯带连不上App怎么办？"},
            {"msg_id": "msg_kf_006", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-02 11:10:00"), "origin": 5, "msgtype": "text", "content": "麻烦把网关断电重启后长按配网键5秒，我同步发您图文教程；仍不行就安排师傅上门调试~"},

            # 增项收费争议
            {"msg_id": "msg_kf_007", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-02 15:15:00"), "origin": 3, "msgtype": "text", "content": "增项我没签字，为什么账单多了3800？"},
            {"msg_id": "msg_kf_008", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-02 15:20:00"), "origin": 5, "msgtype": "text", "content": "已核对，是您爱人现场确认加的厨房拉篮，我补一份签字件给您；如不符可全额退回~"},

            # 甲醛检测报告
            {"msg_id": "msg_kf_009", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-03 10:05:00"), "origin": 3, "msgtype": "text", "content": "甲醛检测报告什么时候给我？"},
            {"msg_id": "msg_kf_010", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-03 10:10:00"), "origin": 5, "msgtype": "text", "content": "CMA报告已出具，主卧0.03mg/m³、客厅0.04mg/m³，均优于国标，原件今天寄出~"},

            # 适老化加装
            {"msg_id": "msg_kf_011", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-03 16:30:00"), "origin": 3, "msgtype": "text", "content": "我妈下个月来住，次卧想加个扶手。"},
            {"msg_id": "msg_kf_012", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-03 16:35:00"), "origin": 5, "msgtype": "text", "content": "已登记为老客户关爱服务，免费加装隐形扶手+地面防滑处理，预计三个工作日内完成~"},

            # 宠物抓花补件
            {"msg_id": "msg_kf_013", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-04 13:40:00"), "origin": 3, "msgtype": "text", "content": "猫把柜门板抓花了，能补一块吗？"},
            {"msg_id": "msg_kf_014", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-04 13:45:00"), "origin": 5, "msgtype": "text", "content": "可以补，单块门板260元；建议同时加装防抓条，老客户价80元每米~"},

            # 保修卡
            {"msg_id": "msg_kf_015", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-05 18:10:00"), "origin": 3, "msgtype": "text", "content": "保修卡丢了，影响保修吗？"},
            {"msg_id": "msg_kf_016", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-05 18:15:00"), "origin": 5, "msgtype": "text", "content": "不影响，我们按合同编号保修，柜体质保十年、五金五年，我给您补发电子保修卡~"},

            # 发票
            {"msg_id": "msg_kf_017", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-06 09:20:00"), "origin": 3, "msgtype": "text", "content": "发票能开成装修服务费吗？"},
            {"msg_id": "msg_kf_018", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-06 09:25:00"), "origin": 5, "msgtype": "text", "content": "可以，按实际项目分单开具；需要专票请提供公司开票信息，我帮您走财务加急~"},

            # 加做餐边柜
            {"msg_id": "msg_kf_019", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-07 10:30:00"), "origin": 3, "msgtype": "text", "content": "我想再加一个餐边柜，多少钱？"},
            {"msg_id": "msg_kf_020", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-07 10:35:00"), "origin": 5, "msgtype": "text", "content": "同色同材质1.2米餐边柜4800元，老客户9折，含上门测量和安装~"},

            # 延期赔付
            {"msg_id": "msg_kf_021", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-08 08:00:00"), "origin": 3, "msgtype": "text", "content": "你们延期了6天，按合同怎么赔？"},
            {"msg_id": "msg_kf_022", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-08 08:05:00"), "origin": 5, "msgtype": "text", "content": "确认延期6天，按合同千分之二每天赔付共5016元，将直接抵扣尾款~"},

            # 开荒保洁
            {"msg_id": "msg_kf_023", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-15 19:15:00"), "origin": 3, "msgtype": "text", "content": "开荒保洁什么时候安排？"},
            {"msg_id": "msg_kf_024", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-15 19:20:00"), "origin": 5, "msgtype": "text", "content": "安排在交付后第三天，含全屋开荒和柜体内部除尘，免费赠送~"},

            # 板材检测报告
            {"msg_id": "msg_kf_025", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-16 11:30:00"), "origin": 3, "msgtype": "text", "content": "我想看下当时用的板材检测报告。"},
            {"msg_id": "msg_kf_026", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-06-16 11:35:00"), "origin": 5, "msgtype": "text", "content": "已发送爱格板ENF级检测报告，批号与合同附件一致，您注意查收~"},

            # 转介绍优惠
            {"msg_id": "msg_kf_027", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-08-03 11:00:00"), "origin": 3, "msgtype": "text", "content": "朋友是我推荐来的，有什么优惠？"},
            {"msg_id": "msg_kf_028", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-08-03 11:05:00"), "origin": 5, "msgtype": "text", "content": "老客户转介绍可享同款方案92折，并赠送全屋除甲醛一次~"},

            # 年度保养
            {"msg_id": "msg_kf_029", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-08-05 15:10:00"), "origin": 3, "msgtype": "text", "content": "下次柜体保养大概什么时候？"},
            {"msg_id": "msg_kf_030", "external_id": SAGT_EXTERNAL_ID, "open_kfid": "kf001", "servicer_userid": SAGT_USER_ID, "msg_time": datetime2timestamp("2026-08-05 15:15:00"), "origin": 5, "msgtype": "text", "content": "建议每年一次，明年4月我们会主动联系您预约，老客户免费~"},
        ]
        
        # 批量创建客服消息
        for msg in wxkf_messages:
            try:
                self.store_client.upsert_wxkf_msg(
                    msg_id=msg["msg_id"],
                    external_id=msg["external_id"],
                    open_kfid=msg["open_kfid"],
                    servicer_userid=msg["servicer_userid"],
                    content=msg["content"],
                    msg_time=msg["msg_time"],
                    origin=msg["origin"],
                    msgtype=msg["msgtype"],
                )
                logger.info(f"创建客服消息: {msg['msg_id']}")
            except Exception as e:
                logger.warning(f"客服消息 {msg['msg_id']} 可能已存在: {e}")
        
        logger.info(f"微信客服聊天记录初始化完成，共处理 {len(wxkf_messages)} 条消息")

    def init_orders(self):
        """初始化订单记录"""
        logger.info("正在初始化订单记录...")
        

        # 合同与增项、配套订单记录
        orders = [
            {"union_id": "union001", "order_id": "HT20250928", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2025-09-28 10:00:00"), "order_price": 168000.00, "order_products": ["整装基础合同首款（全屋柜体定制 40%）"], "order_raw_info": {"memo": "签约当天支付，锁定年前排产"}},
            {"union_id": "union001", "order_id": "HT20251105", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2025-11-05 10:00:00"), "order_price": 125000.00, "order_products": ["整装进度款（柜体生产完成 30%）"], "order_raw_info": {"memo": "进场安装前支付"}},
            {"union_id": "union001", "order_id": "HT20260302", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2026-03-02 10:00:00"), "order_price": 83000.00,  "order_products": ["整装尾款（安装验收合格 20%）"], "order_raw_info": {"memo": "已扣除延期赔付 5016 元"}},
            {"union_id": "union001", "order_id": "HT20260318", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2026-03-18 10:00:00"), "order_price": 12800.00,  "order_products": ["厨房拉篮升级", "餐边柜增项"], "order_raw_info": {"memo": "现场由客户爱人确认，后补签字件"}},
            {"union_id": "union001", "order_id": "HT20260410", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2026-04-10 10:00:00"), "order_price": 26800.00,  "order_products": ["厨房家电包（烟灶套装+洗碗机+嵌入式蒸烤箱）"], "order_raw_info": {"memo": "客户要求与柜体同色面板"}},
            {"union_id": "union001", "order_id": "HT20260506", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2026-05-06 10:00:00"), "order_price": 18600.00,  "order_products": ["软装包（窗帘+地毯+主卧床品四件套）"], "order_raw_info": {"memo": "风格盐系原木，客户指定色号"}},
            {"union_id": "union001", "order_id": "HT20260612", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2026-06-12 10:00:00"), "order_price": 9800.00,   "order_products": ["智能家居包（全屋灯带+网关+场景面板）"], "order_raw_info": {"memo": "需与App配网，已安排上门调试"}},
            {"union_id": "union001", "order_id": "HT20260708", "open_id": "open001", "order_status": 100,"order_create_time": datetime2timestamp("2026-07-08 10:00:00"), "order_price": 3980.00,   "order_products": ["延保服务包（延保三年+每年一次柜体保养）"], "order_raw_info": {"memo": "老客户专享价"}},
        ]
        
        # 批量创建订单
        for order in orders:
            try:
                self.store_client.upsert_wxxd_order(
                    union_id=order["union_id"],
                    order_id=order["order_id"],
                    open_id=order["open_id"],
                    order_status=order["order_status"],
                    order_products=order["order_products"],
                    order_price=order["order_price"],
                    order_create_time=order["order_create_time"],
                    order_raw_info=order["order_raw_info"],
                )
                logger.info(f"创建订单: {order['order_id']} - {order['order_products']}")
            except Exception as e:
                logger.warning(f"订单 {order['order_id']} 可能已存在: {e}")
        
        logger.info(f"订单记录初始化完成，共处理 {len(orders)} 个订单")


# 主函数和命令行入口
def main():
    """主函数"""
    initializer = DemoDataInitializer(SAGT_SERVER_URL, SAGT_USER_ID, SAGT_USER_PASSWORD)
    #initializer.init_tags()
    #initializer.init_user_and_customer()
    #initializer.init_wxqy_messages()
    #initializer.init_wxkf_messages()
    #initializer.init_orders()
    initializer.init_all_data()
    

if __name__ == "__main__":
    # 运行初始化脚本
    main()
