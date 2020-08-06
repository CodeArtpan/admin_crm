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

    def self_define(self):
        data_list = models.UserInfo.objects.filter(id__gt=7)
        return data_list

    model_form_class = UserInfoModelForm
    list_filter = [
        v1.FilterOptionConfig('ug', True),
        v1.FilterOptionConfig('roles', False),
        v1.FilterOptionConfig('username', False, lambda x: x.username, lambda x: x.username),
        v1.FilterOptionConfig(self_define, False),
    ]

    """
        用于在创建组合搜索
            1. 搜索元素必须是FilterOptionConfig对象
            2. FilterOption参数：
                    - :param field: 字段名称或函数
                    - :param is_multi: 是否支持多选
                    - :param text_func_name: 在Model中定义函数，显示文本名称，默认使用 str(对象)
                    - :param val_func_name:  在Model中定义函数，显示文本名称，默认使用 对象.pk
            示例一：

                    list_filter = [
                        v1.FilterOptionConfig('username', False),
                        v1.FilterOptionConfig('fk', False),
                        v1.FilterOptionConfig('mm', False),
                    ]

            示例二：
                    list_filter = [
                        v1.FilterOptionConfig('username', False,text_func_name=arya_filter_fk_text,value_func_name=arya_filter_fk_name),
                        v1.FilterOptionConfig('fk', False),
                        v1.FilterOptionConfig('mm', False),
                    ]

                    class UserInfo(models.Model):
                        username = models.CharField(verbose_name='用户名',max_length=32)
                        pwd = models.CharField(verbose_name='密码',max_length=32)
                        fk = models.ForeignKey(verbose_name='用户组',to=UserGroup,null=True)
                        mm = models.ManyToManyField(verbose_name='选多个',to=Some)

                        def arya_filter_fk_text(self):
                            return self.username

                        def arya_filter_fk_name(self):
                            return self.username

            示例三：
                    def custom():
                        data_list = models.XX.objects.all()
                        return data_list


                    list_filter = [
                        v1.FilterOptionConfig('username'),
                        v1.FilterOptionConfig(custom, False),
                    ]
            示例四：
                    def custom():
                        data_list = models.XX.objects.all()
                        return data_list


                    list_filter = [
                        v1.FilterOptionConfig('username'),
                        v1.FilterOptionConfig(custom, False，text_func_name=arya_filter_nnn_text,value_func_name=arya_filter_nnn_name),
                    ]

                    class XX(models.Model):
                        ... = models.CharField(verbose_name='用户名',max_length=32)

                        def arya_filter_nnn_text(self):
                            return self.username

                        def arya_filter_nnn_name(self):
                            return self.username

            """


class RoleConfig(v1.CrmSetting):
    list_display = ['id', 'caption']


class UgConfig(v1.CrmSetting):
    list_display = ['id', 'title']


v1.site.register(models.UserInfo, UserInfoConfig)
v1.site.register(models.Role, RoleConfig)
v1.site.register(models.UserGroup, UgConfig)
