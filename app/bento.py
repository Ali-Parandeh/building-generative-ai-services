import bentoml
from models import load_image_model


@bentoml.service(
    resources={"cpu": "4"}, traffic={"timeout": 120}, http={"port": 5000}
)
class Generate:
    def __init__(self) -> None:
        self.pipe = load_image_model()

    @bentoml.api(route="/generate/image")
    def generate(self, prompt: str) -> str:
        output = self.pipe(prompt, num_inference_steps=10).images[0]
        return output
