from django import template

register = template.Library()

"""
Our first template filter example, for form fields
"""


@register.filter
def field_type(bound_field):
    """
    Helper to get the class name of a form field
    """
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    """
    If the field belongs to a form that is not bound, this will only return form-control as class
    else, it will return invalid or valid based on existence of .errors in the bound_field object
    """
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {css_class}'.format(css_class=css_class)
