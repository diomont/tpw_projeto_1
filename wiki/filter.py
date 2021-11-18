from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  return value.split(key)

@register.filter(name='find')
def find(value, key):
  """
    Returns the idx of key on value string
  """
  return value.find(key)

@register.filter(name='substring')
def substring(value, key):
  """
    Returns string from key[0] to key[1]
  """
  print("value:", value)
  print("key:", key)
  return value[0:int(key)]
  # print("value:", value)
  # print("key:", key)
  # return "sus"

@register.filter(name='updatedata')
def update_data(value):
  data = value
  return data