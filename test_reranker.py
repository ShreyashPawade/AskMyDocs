from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

question = "What is Strength of Figure?"

chunk = """
Accuracy is closeness of measured value to true value.
"""

score = reranker.predict(
    [
        (question, chunk)
    ]
)

print(score)