from django.template.library import Library
from django.forms.models import ModelChoiceField
from django.forms.boundfield import BoundField
from django.urls import reverse
from crm.service.v1 import site
register = Library()


def temp_gen(model_form_obj):
    for item in model_form_obj:
        field_info = {'tag': item, 'has_popup': False, 'popup_url': None}
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in site._registry:
            field_info['has_popup'] = True
            field_class = item.field.queryset.model
            app_label = field_class._meta.app_label
            model_name = field_class._meta.model_name
            url = reverse("{0}:{1}_{2}_add".format(site.namespace, app_label, model_name))
            popup_url = "{0}?_popup={1}".format(url, item.auto_id)
            field_info['popup_url'] = popup_url
        yield field_info


@register.inclusion_tag('add_form.html')
def show_add_form_data(model_form_obj):
    return {'model_form_obj': temp_gen(model_form_obj)}
