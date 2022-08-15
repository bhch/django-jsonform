from importlib import import_module
from django.http import JsonResponse, HttpResponseNotAllowed
from django.conf import settings


if hasattr(settings, 'JSONFORM_UPLOAD_HANDLER'):
    # 'JSONFORM_UPLOAD_HANDLER' setting is deprecated.
    # We still do this check for backwards compatibility.
    module_path, handler_func = settings.JSONFORM_UPLOAD_HANDLER.rsplit('.', 1)
    FILE_UPLOAD_HANDLER = getattr(import_module(module_path), handler_func)
else:
    FILE_UPLOAD_HANDLER = None


def upload_handler(request):
    if request.method == 'POST':
        if not FILE_UPLOAD_HANDLER:
            return JsonResponse({'error': 'File handler not provided'})
        file_path = FILE_UPLOAD_HANDLER(request)
        return JsonResponse({'value': file_path})
    elif request.method == 'GET':
        return JsonResponse({'results': []})
    return HttpResponseNotAllowed(['POST'], '405 Method Not Allowed')
