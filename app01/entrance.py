from crm.service import v1
from . import models
from django.forms import ModelForm
from django.forms import widgets as form_wg


class Permission(object):
    def get_show_add_btn(self):
        return False


class UserInfoConfig(v1.CrmSetting):
    list_display = ['id', 'username', 'password', 'ug']

    def initial(self):
        pass
    initial.short_desc = '初始化'
    actions = [initial, ]

    class UserInfoModelForm(ModelForm):
        class Meta:
            model = models.UserInfo
            fields = '__all__'
            widgets = {
                'username': form_wg.TextInput(attrs={'class': 'form-control'}),
                'password': form_wg.TextInput(attrs={'class': 'form-control'}),
            }

    model_form_class = UserInfoModelForm


class RoleConfig(v1.CrmSetting):
    list_display = ['id', 'caption']


class UgConfig(v1.CrmSetting):
    list_display = ['id', 'title']


v1.site.register(models.UserInfo, UserInfoConfig)
v1.site.register(models.Role, RoleConfig)
v1.site.register(models.UserGroup, UgConfig)
