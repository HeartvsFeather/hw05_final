from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    template = 'core/404.html'
    context = {
        'path': request.path
    }
    return render(request, template, context, status=HTTPStatus.NOT_FOUND)


def forbidden(request, exception):
    template = 'core/403.html'
    return render(request, template, status=HTTPStatus.FORBIDDEN)


def interna_server_error(request, reason=''):
    template = 'core/500.html'
    return render(request, template, status=HTTPStatus.INTERNAL_SERVER_ERROR)
