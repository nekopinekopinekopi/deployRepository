from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.utils import timezone






# カスタムユーザーを使う際は、オーバーライド必須なマネージャーの関数。
# natural keyは、データベース内のレコードをユニークに識別するための自然な方法を提供する機能
# **get_by_natural_key**は、natural key機能を使用する際に利用されるメソッド。
class UserManager(BaseUserManager):
    
    def get_by_natural_key(self, username):
        return self.get(username=username)



class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_addはオブジェクトが最初に作成されるとき、自動的にフィールドに現在の日付をセットします。
    update_at = models.DateTimeField(auto_now=True)  # auto_nowはオブジェクトが保存される度に自動的に現在の日付をセットします。

    objects = UserManager()

    USERNAME_FIELD = "username"  # ユーザーを一意に識別するフィールドの指定

    def natural_key(self):
        return (self.username,)
