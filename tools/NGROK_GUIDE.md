# 🌐 Ngrok Setup Guide (1分钟搞定)

**用途：** 把本机的FreeLLMAPI服务暴露到公网，让客户可以直接调用你的AI API。

**操作：**

1️⃣ 手机打开 https://dashboard.ngrok.com/signup

2️⃣ 注册（用QQ邮箱，免费版够用）

3️⃣ 进 Dashboard → 复制你的 **Auth Token**

4️⃣ **把token发给我**，我执行：
   ```
   ngrok config add-authtoken <你的token>
   ngrok http 3100
   ```

完成后：
- 得到一个 `https://xxxx.ngrok-free.app` 的公开地址
- 别人可以通过这个地址调用你的98模型API
- 可以封装成API转售服务（¥19/月）
