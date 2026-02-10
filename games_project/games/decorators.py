# sets field title in admin panel instead of .short_description or .title
def title(text):
    def wrapper(obj):
        obj.short_description = text
        obj.title = text
        return obj

    return wrapper
