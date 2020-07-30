from django.urls import path, re_path
from django.shortcuts import render, HttpResponse


class ChangeList(object):
    def __init__(self, data_list, list_display, model_config_obj):
        self.data_list = data_list
        self.list_display = list_display
        self.model_config_obj = model_config_obj


class CrmSetting(object):
    """
    基础配置类
    """
    list_display = []

    def __init__(self, model_class, crm_site):
        self.model_class = model_class
        self.crm_site = crm_site

    def changelist_view(self, request, *args, **kwargs):
        data_list = self.model_class.objects.all()
        cl = ChangeList(data_list, self.list_display, self)
        context = {'cl': cl}
        return render(request, 'changelist.html', context)

    def add_view(self, request, *args, **kwargs):
        return HttpResponse('添加页面')

    def delete_view(self, request, *args, **kwargs):
        return HttpResponse('删除页面')

    def change_view(self, request, *args, **kwargs):
        return HttpResponse('修改页面')

    def get_urls(self):
        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        url_patterns = [
            re_path(r'^$', self.changelist_view, name='%s_%s_changelist' % app_model_name),
            re_path(r'^add/$', self.add_view, name='%s_%s_add' % app_model_name),
            re_path(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % app_model_name),
            re_path(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % app_model_name),
        ]
        url_patterns += self.extra_urls()
        return url_patterns

    def extra_urls(self):
        url = []
        return url

    @property
    def urls(self):
        return self.get_urls(), None, None


class CrmSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, model_setting=None):
        if not model_setting:
            model_setting = CrmSetting
        self._registry[model] = model_setting(model, self)

    def login(self, request, *args, **kwargs):
        return HttpResponse('登陆页面')

    def logout(self, request, *args, **kwargs):
        return HttpResponse('注销页面')

    def get_urls(self):
        url_patterns = []
        url_patterns += [
            path('login/', self.login),
            path('logout/', self.logout),
        ]

        for model_class, model_setting_obj in self._registry.items():
            url_patterns += [
                path('%s/%s/' % (model_class._meta.app_label, model_class._meta.model_name), model_setting_obj.urls)
            ]
        return url_patterns

    @property
    def urls(self):
        return self.get_urls(), None, None


site = CrmSite()
