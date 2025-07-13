from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .utils import retrieve_vector
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


class AskQuestionAPIView(APIView):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
            Handles the question and retrival of the answer
        """
        query = request.data.get("query")
        print("question: ", query)
        retrieved_vector = retrieve_vector(query)
        print("answer: ", retrieved_vector)
        return Response("working...", status=200)
