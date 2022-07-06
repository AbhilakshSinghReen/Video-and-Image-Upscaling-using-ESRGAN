import os

base_dir = os.path.dirname(os.path.dirname(__file__))

models_dir = os.path.join(base_dir, "models")

input_dir = os.path.join(base_dir, "Input")
input_images_dir = os.path.join(input_dir, "Images")
input_videos_dir = os.path.join(input_dir, "Videos")

output_dir = os.path.join(base_dir, "Output")
output_images_dir = os.path.join(output_dir, "Images")
temp_output_videos_dir = os.path.join(output_dir, "Temp Videos")
output_videos_dir = os.path.join(output_dir, "Videos")

def make_dirs_safe():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(output_images_dir):
        os.makedirs(output_images_dir)

    if not os.path.exists(temp_output_videos_dir):
        os.makedirs(temp_output_videos_dir)

    if not os.path.exists(output_videos_dir):
        os.makedirs(output_videos_dir)

def clean_up():
    os.removedirs(temp_output_videos_dir)