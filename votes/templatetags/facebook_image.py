from django import template
from open_facebook import OpenFacebook

register = template.Library()

@register.filter
def fb_image(user):
    if not user.id:
        return False
    
    facebook = OpenFacebook(user.access_token)
    img_url = facebook.my_image_url(size="small")

    return img_url