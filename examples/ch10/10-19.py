from openai import OpenAI

client = OpenAI()

response = client.files.create(
    file=open("mydata.jsonl", "rb"), purpose="fine-tune"
)

client.fine_tuning.jobs.create(
    training_file=response.id, model="gpt-4o-mini-2024-07-18"
)
