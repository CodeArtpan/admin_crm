from django.urls import path, re_path
from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from utils.page import Pagination
import copy
from django.forms import ModelForm
from django.http import QueryDict


class ChangeList(object):
    """
    分装列表页面需要的数据
    """

    def __init__(self, data_list, model_config_obj):
        self.model_config_obj = model_config_obj
        self.list_display = model_config_obj.get_list_display()
        self.actions = model_config_obj.get_actions()
        self.data_list = data_list

        request_get = copy.deepcopy(model_config_obj.request.GET)
        page = Pagination(
            current_page=model_config_obj.request.GET.get('page'),
            total_item_count=data_list.count(),
            base_url=model_config_obj.request.path_info,
            request_params=request_get
        )
        self.data_list = data_list[page.start:page.end]
        self.page_html = page.page_html()

    def add_btn_html(self):
        add_html = '<a href="%s" class="btn btn-xs btn-success">添加</a>'
        app_model_name = self.model_config_obj.app_label, self.model_config_obj.model_name
        url_params = self.model_config_obj.get_changelist_url_params()
        base_url = reverse('crm:%s_%s_add' % app_model_name)
        add_url = '%s?%s' % (base_url, url_params)
        return mark_safe(add_html % add_url)


class CrmSetting(object):
    """
    基础配置类
    """
    list_display = []
    show_add_btn = True
    actions = []
    model_form_class = None

    def __init__(self, model_class, crm_site):
        self.model_class = model_class
        self.crm_site = crm_site
        self.app_label = self.model_class._meta.app_label
        self.model_name = self.model_class._meta.model_name

    def get_reverse_changelist_url(self):
        return reverse('crm:%s_%s_changelist' % (self.app_label, self.model_name))

    def get_changelist_url_params(self):
        request_params = self.request.GET.urlencode()
        query_dict = QueryDict(mutable=True)
        query_dict['changelist_url_params'] = request_params
        return query_dict.urlencode()

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
        base_edit_url = reverse('crm:%s_%s_change' % (self.app_label, self.model_name), args=(obj.pk,))
        base_del_url = reverse('crm:%s_%s_delete' % (self.app_label, self.model_name), args=(obj.pk,))
        url_params = self.get_changelist_url_params()
        edit_url = '%s?%s' % (base_edit_url, url_params)
        del_url = '%s?%s' % (base_del_url, url_params)
        tpl = "<a href='%s' class='btn btn-xs btn-info'>编辑</a> |  \
               <a href='%s' class='btn btn-xs btn-danger'>删除</a>" % (edit_url, del_url)
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
        pk_list = [int(pk) for pk in self.request.POST.getlist('pk')]
        self.model_class.objects.filter(id__in=pk_list).delete()

    multi_del.short_desc = '批量删除'

    def get_actions(self):
        temp = [CrmSetting.multi_del, ]
        temp += self.actions
        return temp

    @property
    def get_model_form_class(self):
        model_form_class = self.model_form_class
        if not model_form_class:
            class DefaultModelForm(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = '__all__'
            model_form_class = DefaultModelForm
        return model_form_class

    def add_view(self, request, *args, **kwargs):
        self.request = request
        params = request.GET.get('changelist_url_params')
        changelist_url = '%s?%s' % (self.get_reverse_changelist_url(), params) if params else \
            self.get_reverse_changelist_url()
        if request.method == 'GET':
            model_form_obj = self.get_model_form_class()
            context = {'model_form_obj': model_form_obj}
            return render(request, 'add_edit.html', context)
        model_form_obj = self.get_model_form_class(request.POST)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect(changelist_url)
        context = {'model_form_obj': model_form_obj}
        return render(request, 'add_edit.html', context)

    def delete_view(self, request, pk, *args, **kwargs):
        self.request = request
        params = request.GET.get('changelist_url_params')
        changelist_url = '%s?%s' % (self.get_reverse_changelist_url(), params) if params else \
            self.get_reverse_changelist_url()
        self.model_class.objects.filter(pk=pk).delete()
        return redirect(changelist_url)

    def change_view(self, request, pk, *args, **kwargs):
        self.request = request
        params = request.GET.get('changelist_url_params')
        changelist_url = '%s?%s' % (self.get_reverse_changelist_url(), params) if params else \
            self.get_reverse_changelist_url()
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return redirect(changelist_url)
        if request.method == 'GET':
            model_form_obj = self.get_model_form_class(instance=obj)
            context = {'model_form_obj': model_form_obj}
            return render(request, 'add_edit.html', context)
        model_form_obj = self.get_model_form_class(request.POST, instance=obj)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect(changelist_url)
        context = {'model_form_obj': model_form_obj}
        return render(request, 'add_edit.html', context)

    def get_urls(self):
        app_model_name = self.app_label, self.model_name
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
    """
    路由构建与分发
    """

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
