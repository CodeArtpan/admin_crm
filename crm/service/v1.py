from django.urls import path, re_path
from django.shortcuts import render, HttpResponse


class CrmSetting(object):
    """
    基础配置类
    """
    list_display = []

    def __init__(self, model_class, crm_site):
        self.model_class = model_class
        self.crm_site = crm_site

    def changelist_view(self, request, *args, **kwargs):
        def headers():
            if not self.list_display:
                yield self.model_class._meta.model_name
            else:
                for v in self.list_display:
                    yield self.model_class._meta.get_field(v).verbose_name if isinstance(v, str) else v(self)
        context = {
            'headers': headers(),
        }
        return render(request, 'changelist.html', context)

    def add_view(self, request, *args, **kwargs):
        return HttpResponse('添加页面')

    def delete_view(self, request, *args, **kwargs):
        return HttpResponse('删除页面')

    def change_view(self, request, *args, **kwargs):
        return HttpResponse('修改页面')

    def get_urls(self):
        url_patterns = [
            re_path(r'^$', self.changelist_view),
            re_path(r'^add/$', self.add_view),
            re_path(r'^(.+)/delete/$', self.delete_view),
            re_path(r'^(.+)/change/$', self.change_view),
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
