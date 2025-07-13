from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import KnowledgeBaseSerializer
from .models import KnowledgeBase


class UploadKnowledgeBase(CreateAPIView):

    http_method_names = ['post']
    serializer_class = KnowledgeBaseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'content' not in request.FILES:
            return Response(
                {"error": "No file provided for the content field."}, status=400
            )
        return super().post(request, *args, **kwargs)
