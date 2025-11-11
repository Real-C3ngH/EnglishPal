import requests
import hashlib
import time
from urllib.parse import urlencode

# 假设这是从某个配置文件中读取的
class BaiduContent:
    APPID = '20240702002090356'
    SECRET = '3CcqcMAJdIIpgG0uMS_f'

def generate_sign(q, salt):
    """生成百度翻译API所需的签名"""
    appid = BaiduContent.APPID
    secret = BaiduContent.SECRET
    appid_with_data = appid + q + salt + secret
    md5_obj = hashlib.md5(appid_with_data.encode('utf-8'))
    return md5_obj.hexdigest()

def translate(q, from_lang, to_lang):
    """调用百度翻译API进行翻译"""
    salt = str(int(time.time()))  # 生成一个时间戳作为salt
    sign = generate_sign(q, salt)

    # 封装请求参数
    params = {
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'appid': BaiduContent.APPID,
        'salt': salt,
        'sign': sign
    }

    # 构造请求URL（百度翻译API使用POST请求，并将参数放在请求体中）
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"

    # 发送POST请求
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = urlencode(params).encode('utf-8')  # 注意：需要编码为bytes

    response = requests.post(url, data=data, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析并返回JSON响应体中的翻译结果
        try:
            return response.json()['trans_result'][0]['dst']
        except (KeyError, IndexError):
            return "Invalid response from API"
    else:
        # 返回错误信息或状态码
        return {"error": f"Failed with status code {response.status_code}"}
