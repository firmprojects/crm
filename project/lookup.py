from ajax_select import register, LookupChannel
from users.models import CustomUser

@register('users')
class TagsLookup(LookupChannel):

    model = CustomUser

    def get_query(self, q, request):
        return self.model.objects.filter(first_name=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name