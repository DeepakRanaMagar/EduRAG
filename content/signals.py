from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import KnowledgeBase

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


@receiver(post_save, sender=KnowledgeBase)
def generate_embedding_from_file(sender, instance, created, **kwargs):
    if created and instance.content:
        try:
            # Read and decode uploaded file
            with instance.content.open("r") as f:
                content = f.read()

            # Generate embedding (included metadata)
            text_to_embed = f"Topic: {instance.topic}. Title: {
                instance.title}. Grade: {instance.grade}. Content: {content}"
            embedding = model.encode(text_to_embed).tolist()

            instance.embedding = embedding
            instance.save(update_fields=["embedding"])

        except Exception as e:
            print(f"Embedding generation failed: {e}")
