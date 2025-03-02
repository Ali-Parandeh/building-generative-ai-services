import time

from openai import OpenAI

client = OpenAI()

question = "what's FastAPI"
for _ in range(2):
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
    )
    print(f"Question: {question}")
    print("Time consuming: {:.2f}s".format(time.time() - start_time))
    print(f"Answer: {response.choices[0].message.content}\n")
