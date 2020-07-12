import random
import re

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from rest_framework.generics import CreateAPIView
from django_redis import get_redis_connection

from bz_edu.libs.geetest import GeetestLib
from bz_edu.settings import constants
from user.models import UserInfo
from user.utils import get_user_by_account
from user.serializers import UserModelSerializer
from utils.send_msg import Message

pc_geetest_id = "6f91b3d2afe94ed29da03c14988fb4ef"
pc_geetest_key = "7a01b1933685931ef5eaf5dabefd3df2"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        """获取验证码"""

        username = request.query_params.get('username')
        user = get_user_by_account(username)
        if user is None:
            return Response({"message": "用户不存在"}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """验证验证码"""
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        # 判断用户是否存在
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)

class UserAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class MobileCheckAPIView(APIView):

    def get(self, request, mobile):
        if not re.match(r"^1[3-9]\d{9}", mobile):
            return Response({"message": "手机号格式不正确"}, status=http_status.HTTP_400_BAD_REQUEST)

        user = get_user_by_account(mobile)

        if user is not None:
            return Response({"message": "手机号已经被注册"}, status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "ok"})


class SendMessageAPIView(APIView):

    def get(self, request, mobile):
        redis_connection = get_redis_connection("sms_code")

        # TODO 1. 判断手机验证码是否在60s内发送过短信
        mobile_code = redis_connection.get("sms_%s" % mobile)
        if mobile_code is not None:
            return Response({"message": "您已经在60s内发送过短息了~"}, status=http_status.HTTP_400_BAD_REQUEST)
        code = "%06d" % random.randint(0, 999999)

        redis_connection.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex("mobile_%s" % mobile, constants.MOBILE_EXPIRE_TIME, code)


        try:
            message = Message(constants.API_KEY)
            message.send_message(mobile, code)
        except:
            return Response({"message": "短信发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)


        return Response({"message": "发送短信成功"}, status=http_status.HTTP_200_OK)

