from openai import AsyncOpenAI
from app.config import settings

# Initialize Groq client using OpenAI-compatible interface
groq_client = AsyncOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url=settings.GROQ_BASE_URL
)


async def generate_answer(query: str, context_docs: list) -> str:
    """Generate answer using Groq LLM with context"""
    try:
        # Prepare context from documents
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            context_parts.append(f"[{i}] {doc['title']}\nURL: {doc['url']}\nContent: {doc['content'][:500]}...\n")

        context = "\n".join(context_parts)

        # Create prompt
        prompt = f"""Based on the following search results, provide a comprehensive answer to the user's question. Use inline citations [1], [2], etc. to reference the sources.

Search Results:
{context}

Question: {query}

Please provide a detailed answer with proper citations. Make sure to:
1. Answer the question thoroughly
2. Use inline citations [1], [2], etc. when referencing information
3. Be factual and accurate
4. Synthesize information from multiple sources when relevant

Answer:"""

        # Generate response using Groq
        response = await groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system",
                 "content": "You are a helpful research assistant that provides accurate, well-cited answers based on search results."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error generating answer: {e}")
        return f"I apologize, but I encountered an error while generating the answer: {str(e)}"
