from django import template

register = template.Library()


@register.filter
def voted_for(user, candidate):
    if not user.is_authenticated():
        return False

    return candidate.voters.filter(id=user.id).exists()


@register.filter
def button_value(user, candidate):
    if candidate.voters.filter(id=user.id).exists():
    	return 0
    return 1
