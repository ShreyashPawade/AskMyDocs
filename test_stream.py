from llm import stream_answer

history = []

for token in stream_answer(
    "What is Strength of Figure?",
    "Strength of Figure is a factor used in triangulation...",
    history
):
    print(token, end="", flush=True)