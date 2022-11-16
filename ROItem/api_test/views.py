import json

from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_test.serializers import UserSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **krgs):
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)


@csrf_exempt
@xframe_options_sameorigin
def testApi(request):
    status = request.POST.get('status')
    print(status)
    if request.body:
        print(type(request.body))
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        print(body_unicode)
        body = json.loads(body_unicode)
        print(body)
        content = body['status']
        print(content)
        ret = {'test': 'testOK', 'status': "OK"}
        return HttpResponse(json.dumps(ret))
    if request.POST:
        ret = {'test': 'testOK2', 'status': "OK2"}
        return HttpResponse(json.dumps(ret))
    ret = {'status': "error"}
    return HttpResponse(json.dumps(ret))
