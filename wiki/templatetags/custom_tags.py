from django import template

register = template.Library()


@register.simple_tag
def link_text(text, start_idx, end_idx):
    idxs = []
    print("start:", start_idx)
    print("end:", end_idx)
    print("text:", text)
    print("output:", text[start_idx:end_idx])

    return text[start_idx:end_idx]


@register.simple_tag
def update_var(value):
    """Updates a variable to value"""
    return value


@register.simple_tag
def teste(value):
    """Updates a variable to value"""
    print("valor foda:", value)
    return value
