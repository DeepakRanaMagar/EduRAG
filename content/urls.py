from django.urls import path


from .views import UploadKnowledgeBase

urlpatterns = [
    path("upload/", UploadKnowledgeBase.as_view(), name="upload_knowledge_base"),
]
