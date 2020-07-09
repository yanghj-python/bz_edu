from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """用户模型"""
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    user_photo = models.ImageField(upload_to="user", verbose_name="用户头像", blank=True, null=True)

    class Meta:
        db_table = "bz_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
