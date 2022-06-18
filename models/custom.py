
from django.http import JsonResponse
import json

def getArgs(func):

    def returnFunc(request):

        if request.method == 'GET':
            args = request.GET.dict()
        elif request.method == 'POST':
            args = request.POST.dict()
            if not args:
                args = json.loads(request.body.decode('utf8'))
        else:
            return response(data_status=500, data_msg='faild', results='please use post or get method submit requesst')

        return func(args=args)
    return returnFunc

def response(data_status=0, data_msg='ok', results=None,http_status=None, headers=None, exception=False, **kwargs):
    data = {
        'stauts': data_status,
        'msg': data_msg,
    }
    if results is not None:
        data['results'] = str(results)
    else:
        data['results'] = kwargs
    return JsonResponse(data)
