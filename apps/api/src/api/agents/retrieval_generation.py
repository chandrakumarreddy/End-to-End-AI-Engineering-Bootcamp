"""
retrieval generation
"""

import os

from openai import OpenAI
from qdrant_client import QdrantClient


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENAI_API_KEY'),
)

qdrant_client = QdrantClient(url='http://qdrant:6333')


def get_embedding(input_str: str):
    """Get the embedding for the input."""
    embedding = client.embeddings.create(
        model="baai/bge-base-en-v1.5",
        input=input_str,
        encoding_format="float"
    )
    return embedding.data[0].embedding


def retrieve_data(input_str: str):
    """Retrieve the data for the input."""
    query_embedding = get_embedding(input_str)

    results = qdrant_client.query_points(
        collection_name="Amazon-items-collection",
        query=query_embedding,
        with_payload=True,
        limit=5
    ).points

    retrieved_context_ids = []
    retrieved_context = []
    similarity_scores = []
    retrieved_context_ratings = []

    for result in results:
        if result.payload is None:
            continue
        retrieved_context_ids.append(result.payload["parent_asin"])
        retrieved_context.append(result.payload["description"])
        retrieved_context_ratings.append(result.payload["average_rating"])
        similarity_scores.append(result.score)

    return {
        "retrieved_context_ids": retrieved_context_ids,
        "retrieved_context": retrieved_context,
        "retrieved_context_ratings": retrieved_context_ratings,
        "similarity_scores": similarity_scores,
    }


def process_context(context):
    """Process the retrieved context."""
    formatted_context = ""
    for context_id, description, rating in zip(context["retrieved_context_ids"], context["retrieved_context"], context["retrieved_context_ratings"]):
        formatted_context += f"- ID: {context_id}, rating: {rating}, description: {description}\n"
    return formatted_context


def build_prompt(question, context):
    """Build the prompt for the LLM."""
    return f"""You are ai shopping assistant that can answer question about the products in stock
You will be given a question and context.
Instructions:
1. You need to asnwer based on the context only
2. never use the word context and refer it as available product

Context:
{context}

Question:
{question}"""


def generate_answer(prompt):
    """Generate answer using LLM."""
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[{"role": "system", "content": prompt}],
        extra_body={"reasoning": {"enabled": False}}
    )
    return response.choices[0].message.content


def rag_pipeline(question):
    """RAG pipeline."""
    retrieved_context = retrieve_data(question)
    preprocessed_context = process_context(retrieved_context)
    prompt = build_prompt(question, preprocessed_context)
    answer = generate_answer(prompt)

    return answer
