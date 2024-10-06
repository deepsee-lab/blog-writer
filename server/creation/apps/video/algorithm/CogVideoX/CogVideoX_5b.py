import os
import gc
import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video
from dotenv import load_dotenv

load_dotenv()

model_name = "THUDM/CogVideoX-5b"
base_model_dir = os.getenv("BASE_LVM_MODEL_DIR")
print(base_model_dir)
model_path = os.path.join(base_model_dir, model_name)
print('model_path: {}'.format(model_path))


def get_output_dir():
    output_file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir, exist_ok=True)
    return output_file_dir


def inf(prompt, filename):
    pipe = CogVideoXPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16
    )

    pipe.enable_model_cpu_offload()
    pipe.vae.enable_tiling()

    video = pipe(
        prompt=prompt,
        num_videos_per_prompt=1,
        num_inference_steps=50,
        num_frames=49,
        guidance_scale=6,
        generator=torch.Generator(device="cuda").manual_seed(42),
    ).frames[0]

    output_file = '{}/{}.mp4'.format(get_output_dir(), filename)

    export_to_video(video, output_file, fps=8)

    # 删除并尝试释放内存
    del video
    del pipe

    gc.collect()
    torch.cuda.empty_cache()

    return output_file


def run():
    filename = 'demo'
    prompt = "A panda, dressed in a small, red jacket and a tiny hat, sits on a wooden stool in a serene bamboo forest. The panda's fluffy paws strum a miniature acoustic guitar, producing soft, melodic tunes. Nearby, a few other pandas gather, watching curiously and some clapping in rhythm. Sunlight filters through the tall bamboo, casting a gentle glow on the scene. The panda's face is expressive, showing concentration and joy as it plays. The background includes a small, flowing stream and vibrant green foliage, enhancing the peaceful and magical atmosphere of this unique musical performance."

    inf(prompt, filename)


if __name__ == '__main__':
    import time

    time1 = time.time()

    run()

    time2 = time.time()

    print(f'total time: {time2 - time1}')
