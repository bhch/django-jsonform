from importlib import import_module
from django.http import JsonResponse, HttpResponseNotAllowed
from django.conf import settings


def upload_handler(request):
    if request.method == 'POST':
        module_path, handler_func = settings.JSONFORM_UPLOAD_HANDLER.rsplit('.', 1)
        func = getattr(import_module(module_path), handler_func)
        file_path = func(request)
        return JsonResponse({'file_path': file_path})
    return HttpResponseNotAllowed(['POST'], '405 Method Not Allowed')
