from django import template

register = template.Library()


@register.filter
def voted_for(user, candidate):
    if not user.id:
        return False
    
    return candidate.users.filter(id=user.id).exists()
