from django.core.urlresolvers import resolve, Resolver404

# Custom context managers for templates

# adds {{ appname }} template tag to templates
def appname(request):
    try:
        app_label = resolve(request.path).app_name
    except Resolver404:
        app_label = None
    return {'appname': app_label}