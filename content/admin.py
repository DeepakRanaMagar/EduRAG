from django.contrib import admin

from .models import KnowledgeBase


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "grade", "topic", "embedding_summary")

    def embedding_summary(self, obj):
        if obj.embedding is None:
            return "None"
        return f"{len(obj.embedding)}-dim vector"
