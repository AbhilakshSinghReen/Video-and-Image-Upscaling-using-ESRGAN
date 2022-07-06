import os
import shutil
import cv2
import moviepy.editor as mpe


from upscale import upscale_block
from split_frame import split_image_into_blocks
from combine_frame import combine_blocks_into_image

from dirs import input_images_dir, input_videos_dir, output_images_dir, output_videos_dir, temp_output_videos_dir, make_dirs_safe, clean_up

def printImage(img):
    x = 0
    for r in img:
        for c in r:
            x += 1
            if (x % 10000 == 0):
                print(c)

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = ' ' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end = "\r")

def upscale_single_frame(frame):
    blocks_data = split_image_into_blocks(frame, (300, 300))

    for i in range(0, len(blocks_data[1])):
        # progress_bar(i + 1, len(blocks_data[1]))
        blocks_data[1][i] = upscale_block(blocks_data[1][i])

    frame = combine_blocks_into_image(blocks_data)

    return frame

def read_and_upscale_single_image(input_path, output_path):
    print()
    print(f"Upscaling: {input_path}")

    image = cv2.imread(input_path)
    ############################
    # printImage(image)
    # return

    image = upscale_single_frame(image)

    cv2.imwrite(output_path, image)

def read_and_upscale_single_video(input_path, output_path):
    print()
    print(f"Upscaling: {input_path}")
    temp_output_path = os.path.join(temp_output_videos_dir, os.path.basename(output_path))
    temp_images_dir = os.path.join(temp_output_videos_dir, "Temp Video Frames")
    if not os.path.exists(temp_images_dir):
        os.makedirs(temp_images_dir)

    cap = cv2.VideoCapture(input_path)

    ret, frame = cap.read()   
        
    if not ret:
        cap.release()
        return

    frame1_upscaled = upscale_single_frame(frame)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (frame1_upscaled.shape[1], frame1_upscaled.shape[0])
    # print(size)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    writer = cv2.VideoWriter(temp_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    frame_count = 0

    while True:
        frame_count += 1
        ############################
        
        # if (frame_count > 10):
        #     # printImage(frame)
        #     break
        # # print(frame_count)

        progress_bar(frame_count, total_frames)

        frame = upscale_single_frame(frame)

        temp_image_path = os.path.join(temp_images_dir, f"f{frame_count}.png")
        cv2.imwrite(temp_image_path, frame)
        frame = cv2.imread(temp_image_path)
        
        # print(frame.shape)
        cv2.imshow("ok",frame)
        writer.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        ret, frame = cap.read()
        
        if not ret:
            break
    
    shutil.rmtree(temp_images_dir)
    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    ## Attach audio
    originalAudio = mpe.VideoFileClip(input_path).audio
    newClip = mpe.VideoFileClip(temp_output_path)

    newClip.audio = originalAudio
    newClip.write_videofile(output_path)

    # os.remove(temp_output_path)

if __name__ == "__main__":
    make_dirs_safe()

    input_images_paths = os.listdir(input_images_dir)
    for input_image_path in input_images_paths:
        read_and_upscale_single_image(os.path.join(input_images_dir, input_image_path), os.path.join(output_images_dir, input_image_path))

    input_video_paths = os.listdir(input_videos_dir)
    for input_video_path in input_video_paths:
        read_and_upscale_single_video(os.path.join(input_videos_dir, input_video_path), os.path.join(output_videos_dir, input_video_path))

    clean_up()



'''
On my GTX 1650, it took around 12 secs per frame to convert from (960x540) to 4k.
So, to make a 10 min 4k 60 FPS video, it will take around 432,000 secs or 5 days.
'''