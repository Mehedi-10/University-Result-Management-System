from django import template

register = template.Library()


@register.filter
def is_blocked(dic):
    return dic[len(dic)-1].Student_id=="~~THE_END~~"

@register.filter
def dicfast(dic):
    tmpdic=dic.copy()
    if is_blocked(tmpdic):
        tmpdic.popitem()
    return tmpdic.items()


