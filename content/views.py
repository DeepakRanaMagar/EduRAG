from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .utils import retrieve_vector, generate_answer_from_api
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
        personas = ['friendly', 'strict', 'humorous']
        persona = request.data.get("persona")
        if persona not in personas:
            return Response({"error": f"Persona should be one of {personas}"}, status=400)

        retrieved_vector = retrieve_vector(query)
        if not retrieved_vector.exists():
            return Response({"message": "Sorry, No Information found in the request query."}, status=400)

        context = "\n\n".join([
            doc.content.read().decode('utf-8') if hasattr(doc.content,
                                                          'read') else open(doc.content.path).read()
            for doc in retrieved_vector
        ])
        answer = generate_answer_from_api(context, query, persona)
        data = {
            "message": answer
        }
        return Response(data, status=200)


class TopicsListView(ListAPIView):
    serializer_class = KnowledgeBaseSerializer
    http_method_names = ['get']

    def get_queryset(self):
        grade = self.request.query_params.get('grade')

        qs = KnowledgeBase.objects.all()

        if grade:
            qs = qs.filter(grade=grade)

        return qs.values('topic').distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        topics = [item['topic'] for item in queryset]
        return Response({"topics": topics}, status=200)


class MetricsView(APIView):
    def get(self, request):
        total_topics = KnowledgeBase.objects.values(
            "topic").distinct().count()
        total_files = KnowledgeBase.objects.count()
        total_grades = KnowledgeBase.objects.values(
            "grade").distinct().count()

        return Response({
            "total_topics": total_topics,
            "total_files_uploaded": total_files,
            "total_grades": total_grades
        }, status=200)
