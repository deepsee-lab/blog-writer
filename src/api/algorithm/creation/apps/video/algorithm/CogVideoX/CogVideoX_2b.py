import os
import gc
import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video
from dotenv import load_dotenv

load_dotenv()

model_name = "THUDM/CogVideoX-2b"
base_model_dir = os.getenv("BASE_LVM_MODEL_DIR")
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
        torch_dtype=torch.float16
    ).to("cuda")

    prompt_embeds, _ = pipe.encode_prompt(
        prompt=prompt,
        do_classifier_free_guidance=True,
        num_videos_per_prompt=1,
        max_sequence_length=226,
        device="cuda",
        dtype=torch.float16,
    )
    video = pipe(
        num_inference_steps=50,
        guidance_scale=6,
        prompt_embeds=prompt_embeds,
    ).frames[0]

    output_file = '{}/{}.mp4'.format(get_output_dir(), filename)
    print('------------')
    export_to_video(video, output_file, fps=8)

    # 删除并尝试释放内存
    del prompt_embeds
    del video
    del pipe

    gc.collect()
    torch.cuda.empty_cache()

    return output_file


def run():
    filename = 'demo'

    # prompt = "A panda, dressed in a small, red jacket and a tiny hat, sits on a wooden stool in a serene bamboo forest. The panda's fluffy paws strum a miniature acoustic guitar, producing soft, melodic tunes. Nearby, a few other pandas gather, watching curiously and some clapping in rhythm. Sunlight filters through the tall bamboo, casting a gentle glow on the scene. The panda's face is expressive, showing concentration and joy as it plays. The background includes a small, flowing stream and vibrant green foliage, enhancing the peaceful and magical atmosphere of this unique musical performance."
    # prompt = "A detailed wooden toy ship with intricately carved masts and sails is seen gliding smoothly over a plush, blue carpet that mimics the waves of the sea. The ship's hull is painted a rich brown, with tiny windows. The carpet, soft and textured, provides a perfect backdrop, resembling an oceanic expanse. Surrounding the ship are various other toys and children's items, hinting at a playful environment. The scene captures the innocence and imagination of childhood, with the toy ship's journey symbolizing endless adventures in a whimsical, indoor setting."
    # prompt = "The camera follows behind a white vintage SUV with a black roof rack as it speeds up a steep dirt road surrounded by pine trees on a steep mountain slope, dust kicks up from it’s tires, the sunlight shines on the SUV as it speeds along the dirt road, casting a warm glow over the scene. The dirt road curves gently into the distance, with no other cars or vehicles in sight. The trees on either side of the road are redwoods, with patches of greenery scattered throughout. The car is seen from the rear following the curve with ease, making it seem as if it is on a rugged drive through the rugged terrain. The dirt road itself is surrounded by steep hills and mountains, with a clear blue sky above with wispy clouds."
    # prompt = "A street artist, clad in a worn-out denim jacket and a colorful bandana, stands before a vast concrete wall in the heart, holding a can of spray paint, spray-painting a colorful bird on a mottled wall."
    # prompt = "In the haunting backdrop of a war-torn city, where ruins and crumbled walls tell a story of devastation, a poignant close-up frames a young girl. Her face is smudged with ash, a silent testament to the chaos around her. Her eyes glistening with a mix of sorrow and resilience, capturing the raw emotion of a world that has lost its innocence to the ravages of conflict."
    # prompt = "Beautiful wedding scene"
    prompt = "Create a breathtaking fantasy video that captures the essence of a 'Genshin Impact'-like universe. The scene starts in a vibrant, lush forest with a diverse array of bioluminescent plants and mystical creatures. As the camera moves, it reveals a hidden village with architecture inspired by a blend of medieval European and East Asian styles. Throughout the video, introduce characters with unique, elemental-based abilities interacting with their environment, showcasing their powers in dramatic, visually stunning ways. Incorporate a soothing, enchanting soundtrack that complements the ethereal visuals."

    inf(prompt, filename)


if __name__ == '__main__':
    import time

    time1 = time.time()

    run()

    time2 = time.time()

    print(f'total time: {time2 - time1}')
