from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import KnowledgeBaseSerializer
from .models import KnowledgeBase


class UploadKnowledgeBase(APIView):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        return Response("working....", status=200)
