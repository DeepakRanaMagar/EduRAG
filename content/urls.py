from django.urls import path


from .views import UploadKnowledgeBase, AskQuestionAPIView

urlpatterns = [
    path("upload/", UploadKnowledgeBase.as_view(), name="upload_knowledge_base"),
    path("ask/", AskQuestionAPIView.as_view(), name="ask_question"),
]
