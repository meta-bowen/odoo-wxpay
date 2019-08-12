# Odoo-wxpay
odoo接入微信SDK - 包括微信支付,微信登陆,微信消息处理
# 安装

使用pip
```
sudo pip install weixin-python
```
使用easy_install
```
sudo easy_install weixin-python
```
# 功能
- 微信（静默）网页授权
- 微信支付
- 微信支付回调通知

# 异常
父异常类名为 WeixinError 子异常类名分别为 WeixinLoginError WeixinPayError WeixinMPError WeixinMsgError

# 用法
## 参数
- WEIXIN_MCH_ID 必填，微信商户ID，纯数字
- WEIXIN_MCH_KEY 必填，微信商户KEY
- WEIXIN_NOTIFY_URL 必填，微信回调地址
- WEIXIN_APP_ID 必填，微信公众号appid
- WEIXIN_APP_SECRET 必填，微信公众号appkey
- ENCODE_URL 必填，网站域名的encodeURLComponent
- BASE_URL 必填，网站基础目录
## back-end代码
back-end文件中所有代码均存放在后端controllers文件中
## front-end代码
buy.js文件作为前端点击事件，当点击支付按钮时执行该代码块。故需将此代码植入到前端支付按钮点击事件中，请自行调配！
