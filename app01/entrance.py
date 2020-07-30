from crm.service import v1
from . import models
from django.utils.safestring import mark_safe
from django.urls import reverse


class UserInfoConfig(v1.CrmSetting):
    def check(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" id="%s">' % obj.pk)

    def option(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        tpl = "<a href='%s' class='btn btn-xs btn-info'>编辑</a> |  \
               <a href='%s' class='btn btn-xs btn-danger'>删除</a>"\
            % (reverse('app01_userinfo_changelist'), reverse('app01_userinfo_delete', args=(obj.pk, )))
        return mark_safe(tpl)

    list_display = [check, 'id', 'username', 'password', option]


v1.site.register(models.UserInfo, UserInfoConfig)
