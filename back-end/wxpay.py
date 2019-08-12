from odoo import http
from odoo.http import request
import json
from urllib import parse
from . import config

"""
微信登陆
"""
from datetime import datetime, timedelta
from weixin.login import WeixinLogin

"""
微信支付
"""
from weixin.pay import WeixinPay, WeixinPayError




class WxPay(http.Controller):

    def __init__(self):
        self.app_id = config.APPID
        self.app_secret = config.APP_SECRTET
        self.mch_id = config.MCH_ID
        self.mch_key = config.MCH_KEY

        # url处理
        self.encodeURL = config.encodeURL
        self.URL = config.URL
        self.base_url = config.base_url
        self.notify_url = config.notify_url

        # 初始化
        wx_login = WeixinLogin(self.app_id, self.app_secret)
        wx_pay = WeixinPay(self.app_id, self.mch_id, self.mch_key, self.notify_url)
    @http.route("/odoo/login/<param>", auth="public", website=True)
    def login(self, param, **kwargs):
        """
        微信获取code
        :param param: 传入参数名（非字典、列表）
        :return:
        """
        redirect_url = self.URL + param
        openid = request.httprequest.cookies.get("openid")
        next = request.httprequest.args.get("next") or redirect_url
        if openid:
            return request.redirect(next)
        # callback = url_for("authorized", next=next, _external=True)
        callback = self.encodeURL + "?next=" + next
        url = wx_login.authorize(callback, "snsapi_base")  # 引导用户跳转到授权页面，callback = redirect_uri
        return request.redirect(url)

    @http.route("/odoo/authorized", auth="public", website=True)
    def authorized(self, **kwargs):
        """
        微信验证获取openid
        :return:
        """
        code = request.httprequest.args.get("code")
        if not code:
            return "ERR_INVALID_CODE", 400
        next = request.httprequest.args.get("next")
        data = wx_login.access_token(code)  # 通过code换取网页授权access_token
        openid = data.openid
        resp = request.redirect(next)
        expires = datetime.now() + timedelta(days=1)
        resp.set_cookie("openid", openid, expires=expires)
        return resp

    @http.route("/odoo/pay/create", type="json", auth="public", website=True)
    def pay_create(self, **kwargs):
        """
        微信JSAPI创建统一订单，并且生成参数给JS调用
        必填参数：
            out_trade_no 商户订单号
            body 商品描述
            total_fee 商品描述
            openid 用户标识
        """
        # 网页端调起支付API
        try:
            remote_addr = request.httprequest.environ['REMOTE_ADDR']  # 获取远程客户端IP
            openid = request.httprequest.cookies.get("openid")
            out_trade_no = wx_pay.nonce_str  # 商户订单号设定为随机字符串
            raw = wx_pay.jsapi(openid=openid, body=u"测试", out_trade_no=out_trade_no, total_fee=1, spbill_create_ip=remote_addr)  # 外部传入openid
            return json.dumps(raw)  # 直接返回包含Json格式数据响应的方法
        except WeixinPayError as e:
            print(e.message)
            return e.message, 400

    @http.route("/odoo/pay/notify", auth="public", website=True)
    def pay_notify(self, **kwargs):
        """
        微信异步通知
        """
        data = wx_pay.to_dict(request.data)
        if not wx_pay.check(data):
            return wx_pay.reply("签名验证失败", False)
        return wx_pay.reply("OK", True)  # 处理业务逻辑