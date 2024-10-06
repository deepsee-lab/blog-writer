import os
import gc
import torch
# pip install git+https://github.com/huggingface/diffusers.git
from diffusers import FluxPipeline
from dotenv import load_dotenv

load_dotenv()

# https://github.com/black-forest-labs/flux?tab=readme-ov-file#models
# https://huggingface.co/black-forest-labs/FLUX.1-schnell
model_name = "black-forest-labs/FLUX.1-schnell"
base_model_dir = os.getenv("BASE_LVM_MODEL_DIR")
model_path = os.path.join(base_model_dir, model_name)
print('model_path: {}'.format(model_path))


def get_output_dir():
    output_file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir, exist_ok=True)
    return output_file_dir


def unload_model(pipe):
    # Move model back to CPU
    pipe.to('cpu')

    # Delete model and other large objects
    del pipe
    gc.collect()

    # If using CUDA, clear the CUDA cache
    torch.cuda.empty_cache()


def inf(prompt, filename):
    pipe = FluxPipeline.from_pretrained(model_path, torch_dtype=torch.bfloat16)
    pipe = pipe.to("cuda")
    # pipe.enable_model_cpu_offload()
    # save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

    image = pipe(
        prompt,
        guidance_scale=0.0,
        output_type="pil",
        num_inference_steps=4,
        max_sequence_length=256,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]

    output_file = '{}/{}.png'.format(get_output_dir(), filename)
    image.save(output_file)

    del image
    torch.cuda.empty_cache()

    # 释放模型
    unload_model(pipe)

    return output_file


def run():
    filename = 'demo'
    prompt = "A cat holding a sign that says hello world"
    inf(prompt, filename)


if __name__ == '__main__':
    import time

    time1 = time.time()

    run()

    time2 = time.time()

    print(f'total time: {time2 - time1}')
