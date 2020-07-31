from django.template.library import Library

register = Library()


@register.inclusion_tag('changelist_table.html')
def show_data_list(cl):
    def headers():
        if not cl.list_display:
            yield cl.model_config_obj.model_class._meta.model_name
        else:
            for v in cl.list_display:
                yield cl.model_config_obj.model_class._meta.get_field(v).verbose_name if isinstance(v, str) else v(
                    cl.model_config_obj, is_header=True)

    def body():
        for row in cl.data_list:
            if cl.list_display:
                row_data = []
                for k in cl.list_display:
                    row_data.append(getattr(row, k)) if isinstance(k, str) else row_data.append(
                        k(cl.model_config_obj, obj=row))
                yield row_data
            else:
                yield [str(row), ]

    return {'headers': headers(), 'body': body()}


@register.inclusion_tag('changelist_action.html')
def show_action_list(cl):
    def temp_gen(cl):
        for item in cl.actions:
            yield item.__name__, item.short_desc
    return {'actions': temp_gen(cl)}
