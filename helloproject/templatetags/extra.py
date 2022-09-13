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
        x += 1
    return dic[x:y]


@register.filter
def havemark(c, val):
    if int(c) != int(val):
        return True
    return False


@register.filter
def isempty(li):
    return len(li) == 0


@register.filter
def perdiff(a, b):
    if len(a) == 0:
        a = '0'
    if len(b) == 0:
        b = '0'
    x = int(a)
    y = int(b)
    return abs(x - y) * 100


@register.filter
def multiply(a, b):
    if len(a) == 0:
        a = '0'
    if len(b) == 0:
        b = '0'
    return int(a) * int(b)


@register.filter
def ec_is_empty(a):
    if a == '':
        return 'None'
    else:
        return a


@register.filter
def myavg(a, b):
    if len(a) == 0:
        a = '0'
    if len(b) == 0:
        b = '0'
    return (int(a) + int(b)) / 2
