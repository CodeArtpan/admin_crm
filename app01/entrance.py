from crm.service import v1
from . import models
from django.utils.safestring import mark_safe
from django.urls import reverse


class Permission(object):
    def get_show_add_btn(self):
        return False


class UserInfoConfig(v1.CrmSetting):
    list_display = ['id', 'username', 'password']


class UserGroupConfig(Permission, v1.CrmSetting):
    list_display = ['id', 'title']


v1.site.register(models.UserInfo, UserInfoConfig)
v1.site.register(models.UserGroup, UserGroupConfig)
