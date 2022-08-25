from requests.sessions import session
from django import template

register = template.Library()


@register.filter
def is_blocked(dic):
    return dic[len(dic)-1].Student_id=="~~THE_END~~"

@register.filter
def dicfast(dic):
    return dic.items()
@register.filter
def name(dic):
    x=dic.find('(')
    if x==-1:
        x=len(dic)
    return dic[0:x]

@register.filter
def marks(dic):
    x=dic.find('(')
    y=dic.find(')')
    if x==-1:
        return ""
    else:
        x+=1
    return dic[x:y]
@register.filter
def havemark(c,val):
    if int(c)!=int(val):
        return True
    return False





