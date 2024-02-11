import torch
from PIL import Image
from diffusers import StableDiffusionPipeline
from transformers import pipeline, Pipeline

system_prompt = """
Your name is FastAPI bot and you are a helpful
chatbot responsible for teaching FastAPI to your users.
Always respond in markdown
"""


def load_text_model():
    pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16)
    return pipe


def generate_text(pipe: Pipeline, prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    predictions = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    print(predictions[0]["generated_text"])
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    return output


def load_image_model() -> StableDiffusionPipeline:
    pipe = StableDiffusionPipeline("runwayml/stable-diffusion-v1-5", torch_dtype=torch.bfloat16)
    return pipe


def generate_image(pipe: StableDiffusionPipeline, prompt: str) -> Image.Image:
    output = pipe(prompt).images[0]
    return output
