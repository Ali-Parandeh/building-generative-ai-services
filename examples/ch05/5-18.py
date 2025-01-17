# main.py

from fastapi import BackgroundTasks, FastAPI
import aiofiles

...

app = FastAPI()


async def batch_generate_image(prompt: str, count: int) -> None:
    images = generate_images(prompt, count)
    for i, image in enumerate(images):
        async with aiofiles.open(f"output_{i}.png", mode="wb") as f:
            await f.write(image)


@app.get("/generate/image/background")
def serve_image_model_background_controller(
    background_tasks: BackgroundTasks, prompt: str, count: int
):
    background_tasks.add_task(batch_generate_image, prompt, count)
    return {"message": "Task is being processed in the background"}
