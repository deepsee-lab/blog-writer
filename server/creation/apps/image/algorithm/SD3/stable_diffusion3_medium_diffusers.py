import os
import torch
from diffusers import StableDiffusion3Pipeline
from dotenv import load_dotenv

load_dotenv()

model_name = "stabilityai/stable-diffusion-3-medium-diffusers"
base_model_dir = os.getenv("BASE_LVM_MODEL_DIR")
model_path = os.path.join(base_model_dir, model_name)
print('model_path: {}'.format(model_path))

# 加载模型
pipe = StableDiffusion3Pipeline.from_pretrained(model_path, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

image = pipe(
    prompt="a photo of a cat holding a sign that says hello world",
    negative_prompt="",
    num_inference_steps=28,
    height=1024,
    width=1024,
    guidance_scale=7.0,
).images[0]

image.save("sd3_hello_world.png")
