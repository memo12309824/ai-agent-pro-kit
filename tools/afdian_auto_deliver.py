#!/usr/bin/env python3
"""
爱发电自动交付脚本 — 监听订单并自动发送产品文件
"""

import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================
# 配置
# ============================================
AFDIAN_USER_ID = ""  # 【设置】从爱发电后台获取
AFDIAN_TOKEN = ""    # 【设置】从爱发电后台获取
PRODUCTS = {
    # 商品ID → 产品配置
    "pro": {
        "name": "AI Agent Pro Kit — 专业版",
        "price": 49,
        "delivery": {
            "type": "github_access",
            "repo": "memo12309824/ai-agent-pro-kit",
            "branch": "pro",
            "files": [
                "pro/docker-compose.yml",
                "pro/setup.sh",
                "pro/README.md",
                "pro/config/hermes-integration.yaml",
                "pro/config/exa_search_setup.py",
                "pro/config/agent_reach/profile.yaml"
            ]
        }
    },
    "enterprise": {
        "name": "AI Agent Pro Kit — 企业版",
        "price": 499,
        "delivery": {
            "type": "email",
            "subject": "🎉 欢迎！你的AI Agent Pro Kit企业版已就绪",
            "attachments": []
        }
    }
}

# ============================================
# Webhook 接收 & 验证
# ============================================
class AfdianWebhookHandler(BaseHTTPRequestHandler):
    """接收爱发电订单通知"""
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            if self.verify_signature(data):
                order = self.extract_order(data)
                if order:
                    self.process_order(order)
                self.respond(200, {"ec": 200, "em": "OK"})
            else:
                self.respond(403, {"ec": 403, "em": "Invalid signature"})
        except Exception as e:
            self.respond(500, {"ec": 500, "em": str(e)})
    
    def verify_signature(self, data):
        """验证爱发电回调签名"""
        raw = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        sign = hashlib.md5((raw + AFDIAN_TOKEN).encode()).hexdigest()
        return sign == data.get("sign", "")
    
    def extract_order(self, data):
        """提取订单信息"""
        try:
            order = data.get("data", {}).get("order", {})
            return {
                "order_id": order.get("order_id"),
                "plan_id": order.get("plan_id"),
                "user_id": order.get("user_id"),
                "price": order.get("price", 0),
                "email": order.get("email", ""),
                "status": order.get("status", 0),  # 2=支付成功
            }
        except:
            return None
    
    def process_order(self, order):
        """处理已支付订单"""
        if order["status"] != 2:
            return  # 未支付
        
        plan_id = order["plan_id"]
        email = order["email"]
        
        if plan_id == "pro":
            self.deliver_pro(order)
        elif plan_id == "enterprise":
            self.deliver_enterprise(order)
        
        print(f"✅ 订单 {order['order_id']} 处理完成 → {email}")
    
    def deliver_pro(self, order):
        """发送专业版交付内容"""
        # TODO: 发送GitHub邀请 / 提供下载链接
        pass
    
    def deliver_enterprise(self, order):
        """发送企业版交付内容"""
        # TODO: 邮件发送完整文档包 + 提供技术支持通道
        pass
    
    def respond(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        print(f"[Afdian] {args[0]}")


# ============================================
# 启动
# ============================================
def run_webhook_server(port=17800):
    """启动订单回调服务器"""
    server = HTTPServer(('0.0.0.0', port), AfdianWebhookHandler)
    print(f"🎧 爱发电Webhook监听中 → http://0.0.0.0:{port}")
    print("   在爱发电后台设置回调URL为此地址")
    print("   用ngrok暴露到公网: ngrok http 17800")
    server.serve_forever()


def query_orders(page=1):
    """主动查询未处理的订单（用于轮询而非Webhook）"""
    import requests
    
    ts = int(time.time())
    params = {
        "user_id": AFDIAN_USER_ID,
        "params": json.dumps({"page": page}),
        "ts": ts,
    }
    
    # 签名
    sorted_keys = sorted(params.keys())
    sign_str = AFDIAN_TOKEN
    for k in sorted_keys:
        sign_str += k + str(params[k])
    params["sign"] = hashlib.md5(sign_str.encode()).hexdigest()
    
    resp = requests.post("https://afdian.com/api/open/query-order", json=params)
    return resp.json()


if __name__ == "__main__":
    print("🔧 AI Agent Pro Kit — 爱发电自动交付系统")
    print("=" * 50)
    print("请先配置 AFDIAN_USER_ID 和 AFDIAN_TOKEN")
    print()
    print("启动方式:")
    print("  python afdian_auto_deliver.py  → 启动Webhook服务器")
