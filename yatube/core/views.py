from django.shortcuts import render


def page_not_found(request, exception):
    template = 'core/404.html'
    context = {
        'path': request.path
    }
    return render(request, template, context, status=404)


def forbidden(request, exception):
    template = 'core/403.html'
    return render(request, template, status=403)


def interna_server_error(request, reason=''):
    template = 'core/500.html'
    return render(request, template, status=500)
