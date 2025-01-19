import os
import subprocess


def file_del(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def add_audio_to_video_cli(input_video, input_audio, output_video, overwrite=True):
    if overwrite:
        file_del(output_video)
    shell_command = f'ffmpeg -i "{input_video}" -i "{input_audio}" -c:v copy -c:a aac -strict experimental -shortest "{output_video}"'
    subprocess.run(shell_command, shell=True, check=True)
    if os.path.exists(output_video):
        return True
    else:
        return False
