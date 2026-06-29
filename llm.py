from dotenv import load_dotenv
from google import genai
import os

# -----------------------
# Load Environment
# -----------------------

load_dotenv()

# -----------------------
# Gemini Client
# -----------------------

client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =====================================================
# QUERY REWRITING
# =====================================================

def rewrite_query(
    question,
    chat_history
):
    """
    Rewrite follow-up questions into
    standalone questions.
    """

    if len(chat_history) == 0:
        return question

    history_text = ""

    for item in chat_history[-3:]:

        history_text += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n\n"
        )

    rewrite_prompt = f"""
You are a query rewriting assistant.

Given the conversation history and the current user
question, rewrite the question so that it becomes
fully self-contained.

Conversation:

{history_text}

Current Question:

{question}

Rules:
- Preserve the original meaning.
- Replace pronouns like "it", "they", "this"
  with the correct entity.
- Return ONLY the rewritten question.
- Do not explain anything.
"""

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=rewrite_prompt
    )

    return response.text.strip()


# =====================================================
# ANSWER GENERATION
# =====================================================

def generate_answer(
    question,
    context,
    chat_history
):
    """
    Generate an answer using the
    retrieved context.
    """

    history_text = ""

    for item in chat_history[-5:]:

        history_text += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n\n"
        )
        

    prompt = f"""
You are an intelligent document assistant.

You MUST answer ONLY using the retrieved context.

If the answer is not contained inside
the retrieved context, reply exactly:

"I could not find that information in the documents."

-------------------------
Previous Conversation
-------------------------

{history_text}

-------------------------
Retrieved Context
-------------------------

{context}

-------------------------
Current Question
-------------------------

{question}

Instructions:

- Be concise.
- Use only the retrieved context.
- Do not hallucinate.
- Do not use outside knowledge.
- If formulas are present,
  preserve mathematical notation.
"""

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()



def stream_answer(
    question,
    context,
    
    chat_history
):
    """
    Stream an answer using the
    retrieved context.
    """

    history_text = ""

    for item in chat_history[-5:]:

        history_text += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n\n"
        )

    # Gemini prompt
    prompt = f"""You are an intelligent document assistant.

You MUST answer ONLY using the retrieved context.

If the answer is not contained inside
the retrieved context, reply exactly:

"I could not find that information in the documents."

-------------------------
Previous Conversation
-------------------------

{history_text}

-------------------------
Retrieved Context
-------------------------

{context}

-------------------------
Current Question
-------------------------

{question}

Instructions:

- Be concise.
- Use only the retrieved context.
- Do not hallucinate.
- Do not use outside knowledge.
- If formulas are present,
  preserve mathematical notation.
"""

    response = client_gemini.models.generate_content_stream(
          model="gemini-2.5-flash",
        contents=prompt
    )
    
    for chunk in response:
        if hasattr(chunk,"text") and chunk.text:
            yield chunk.text
        

