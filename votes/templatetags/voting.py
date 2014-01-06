from django import template

register = template.Library()


@register.filter
def voted_for(user, candidate):
    if not user.is_authenticated():
        return False

    return candidate.voters.filter(id=user.id).exists()
