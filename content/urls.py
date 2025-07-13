from django.urls import path


from .views import UploadKnowledgeBase, AskQuestionAPIView, TopicsListView, MetricsView

urlpatterns = [
    path("upload-content/", UploadKnowledgeBase.as_view(),
         name="upload_knowledge_base"),
    path("ask/", AskQuestionAPIView.as_view(), name="ask_question"),
    path("topics/", TopicsListView.as_view(), name="list_topics"),
    path("metrics/", MetricsView.as_view(), name="metrics"),
]
