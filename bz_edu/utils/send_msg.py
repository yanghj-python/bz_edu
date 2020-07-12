import requests
from bz_edu.settings import constants


class Message(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = constants.SINGLE_SEND_URL

    def send_message(self, phone, code):
        params = {
            "apikey": self.api_key,
            'mobile': phone,
            'text': "【杨洪举test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        # 可以发送http请求
        req = requests.post(self.single_send_url, data=params)
        print(req)


if __name__ == '__main__':
    message = Message(constants.API_KEY)
    message.send_message("18736003801", "123456")
