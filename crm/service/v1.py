from django.urls import path, re_path
from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe
from django.urls import reverse


class ChangeList(object):
    """
    分装列表页面需要的数据
    """
    def __init__(self, data_list, model_config_obj):
        self.data_list = data_list
        self.model_config_obj = model_config_obj
        self.list_display = model_config_obj.get_list_display()
        self.actions = model_config_obj.get_actions()

    def add_btn_html(self):
        add_html = '<a href="%s" class="btn btn-xs btn-success">添加</a>'
        app_model_name = self.model_config_obj.model_class._meta.app_label, \
                         self.model_config_obj.model_class._meta.model_name
        add_url = reverse('crm:%s_%s_add' % app_model_name)
        return mark_safe(add_html % add_url)


class CrmSetting(object):
    """
    基础配置类
    """
    list_display = []
    show_add_btn = True
    actions = []

    def __init__(self, model_class, crm_site):
        self.model_class = model_class
        self.crm_site = crm_site

    def changelist_view(self, request, *args, **kwargs):
        self.request = request
        if request.method == 'POST':
            action_name = request.POST.get('action')
            action_func = getattr(self, action_name, None)
            if action_func:
                action_func()
        data_list = self.model_class.objects.all()
        cl = ChangeList(data_list, self)
        context = {'cl': cl}
        return render(request, 'changelist.html', context)

    def checkbox_html(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" value="%s" name="pk">' % obj.pk)

    def option_html(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        tpl = "<a href='%s' class='btn btn-xs btn-info'>编辑</a> |  \
               <a href='%s' class='btn btn-xs btn-danger'>删除</a>"\
            % (reverse('crm:app01_userinfo_change', args=(obj.pk,)), reverse('crm:app01_userinfo_delete', args=(obj.pk,)))
        return mark_safe(tpl)

    def get_list_display(self):
        temp = []
        if self.list_display:
            temp += self.list_display
            temp.insert(0, CrmSetting.checkbox_html)
            temp.append(CrmSetting.option_html)
        return temp

    def get_show_add_btn(self):
        return self.show_add_btn

    def multi_del(self):
        pk_list = [int(pk)for pk in self.request.POST.getlist('pk')]
        self.model_class.objects.filter(id__in=pk_list).delete()

    multi_del.short_desc = '批量删除'

    def get_actions(self):
        temp = [CrmSetting.multi_del, ]
        temp += self.actions
        return temp

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
        self.name = 'crm'
        self.namespace = 'crm'

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
        return self.get_urls(), self.name, self.namespace


site = CrmSite()
