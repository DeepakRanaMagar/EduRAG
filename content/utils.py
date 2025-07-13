from django.db.models import F
from pgvector.django import CosineDistance

from .models import KnowledgeBase
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def retrieve_vector(query, top_k=3):
    '''
        Handles retrival of the vector nearest to the query
    '''
    query_vector = model.encode(query).tolist()
    return KnowledgeBase.objects.annotate(
        similarity=CosineDistance("embedding", query_vector)
    ).order_by('similarity')[:top_k]
