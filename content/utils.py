from sentence_transformers import SentenceTransformer
from django.db.models import F
from pgvector.django import CosineDistance

from .models import KnowledgeBase

from huggingface_hub import InferenceClient
import os

HF_ACCESS_TOKEN = os.getenv('HUGGING_FACE_ACCESS_TOKEN')
client = InferenceClient(
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    token=HF_ACCESS_TOKEN
)


def build_rag_prompt(context: str, question: str, persona: str = "friendly") -> str:
    system_personas = {
        "friendly": "You are a friendly and patient tutor. Use simple words and examples to explain concepts in an encouraging tone.",
        "strict": "You are a strict and academic tutor. Be concise, serious, and precise in your explanations.",
        "humorous": "You are a humorous and witty tutor. Explain the answer while adding clever jokes or light sarcasm to keep it fun.",
    }

    system_prompt = system_personas.get(persona, system_personas["friendly"])

    return f"""<|system|>\n{system_prompt}\n<|user|>\nUse the following context to answer the question:\n\n{context}\n\nQuestion: {question}\n<|assistant|>"""


def generate_answer_from_api(context: str, question: str, persona: str = "friendly", max_tokens: int = 256):
    prompt = build_rag_prompt(context, question, persona)
    response = client.chat_completion(
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Use the following context to answer the question:\n\n{
                context}\n\nQuestion: {question}"}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"]


model = SentenceTransformer('all-MiniLM-L6-v2')


def retrieve_vector(query, top_k=3):
    '''
        Handles retrival of the vector nearest to the query
    '''
    query_vector = model.encode(query).tolist()
    return KnowledgeBase.objects.annotate(
        similarity=CosineDistance("embedding", query_vector)
    ).order_by('similarity')[:top_k]
