// JS点击支付事件拉取微信支付code

_onClick: function () {
        alert('微信支付事件');
        ajax.rpc(this.base_url + "odoo/pay/create",{}).then(function(res){
            var data = JSON.parse(res);
//            this.data_type = typeof(data);
//            console.log('data_type >>> ',this.data_type);
            WeixinJSBridge.invoke(
                'getBrandWCPayRequest', {
                 "appId":data.appId, //公众号名称，由商户传入
                 "timeStamp":data.timeStamp, //时间戳，自1970年以来的秒数
                 "nonceStr":data.nonceStr, //随机串
                 "package":data.package,
                 "signType":data.signType, //微信签名方式
                 "paySign":data.sign, //微信签名
                },
                function(res){
                    if(res.err_msg == "get_brand_wcpay_request:ok" ){
                        console.log("支付成功！");
                        window.location.assign(url) // 该处url指向跳转的页面
                    }else{
                        console.log("支付失败！");
                        alert("支付失败");
                    }
                }
            );
        });
}