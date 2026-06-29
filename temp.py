import os
from vector_store import index_pdf
import os
from vector_store import index_pdf

print("Temp started")

print(os.listdir("docs"))

for file in os.listdir("docs"):

    print("Checking:", file)

    if file.endswith(".pdf"):

        print("Calling index_pdf:", file)

        result = index_pdf(
            os.path.join("docs", file)
        )

        print(result)

