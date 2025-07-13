from django.db import models
from pgvector.django import VectorField


class KnowledgeBase(models.Model):
    topic = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    content = models.FileField(max_length=255, upload_to='contents/%Y/%m/%d/')

    embedding = VectorField(dimensions=768, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.grade}): {self.title}"

    class Meta:
        verbose_name = "KnowledgeBase"
        verbose_name_plural = "KnowledgeBases"
