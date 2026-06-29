from dotenv import load_dotenv
from google import genai

import os
from retriever import hybrid_search
# -----------------------
# Gemini
# -----------------------

load_dotenv()

client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)





# -----------------------
# Ask Question
# -----------------------

def rewrite_query(
    question,
    chat_history,
    client_gemini
):

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

Given the conversation history and
the current user question,

rewrite the question so that it is
fully self-contained.

Conversation:

{history_text}

Current Question:

{question}

Return ONLY the rewritten question.
Do not explain anything.
"""

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=rewrite_prompt
    )

    return response.text.strip()

chat_history = []

while True:

    question = input("\nYou: ")

    if question.lower() in [
        "exit",
        "quit",
        "q"
    ]:
        break

    # Retrieval
    retrieval_question = rewrite_query(
        question,
        chat_history,
        client_gemini
    )

    print(
        f"\nRewritten Query: "
        f"{retrieval_question}"
    )

    context,sources,confidence=hybrid_search(retrieval_question,k=5)
    
    if( confidence<1):
        print("i couldnt confidentaly find an answer in uploaded documenmts ")
        continue

    # Build memory
    history_text = ""

    for item in chat_history[-5:]:

        history_text += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n\n"
        )

    # Gemini prompt
    prompt = f"""
You are a document assistant.

Answer ONLY using the retrieved context.

If the answer is not present in the context, say:

'I could not find that information in the documents.'

Previous Conversation:
{history_text}

Retrieved Context:
{context}

Question:
{question}

Provide a concise answer.
"""

    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    print("\nAnswer:\n")
    print(response.text)
    
    print("\nSources:")

    seen = set()

    for meta in sources:
        source_text=(
            f"{meta['source']}"
            f" (Page {meta['page']})"
        )
        if source_text not in seen:
            print("-",source_text)
            seen.add(source_text)

    chat_history.append(
        {
            "question": question,
            "answer": response.text
        }
    )

print(
    f"\nMemory Size: "
    f"{len(chat_history)}"
)

