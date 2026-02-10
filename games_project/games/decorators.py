# sets field title in admin panel instead of .short_description or .title
def title(text):
    def wrapper(obj):
        obj.short_description = text
        obj.title = text
        return obj

    return wrapper


def remove_delete_actions(admin_class):
    original_get_actions = admin_class.get_actions

    def actions_without_delete(self, request):
        actions = original_get_actions(self, request)
        if "delete_selected" in actions:
            del actions["delete_selected"]

        return actions

    admin_class.get_actions = actions_without_delete

    def remove_delete_permission(self, request, obj=None):
        return False

    admin_class.has_delete_permission = remove_delete_permission

    return admin_class
