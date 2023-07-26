import cv2
import image_preprocessor as ipp
import os
import subprocess, re


def process_video(video_path, output_path):

    command = [
        "ffmpeg", 
        "-y",
        "-i", video_path, 
        "-vf", "cropdetect=24:16:0",  # Detect the black bars
        "-f", "null", 
        "-"
    ]
    
    # Get crop information from the command's output
    crop_info = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
    crop_line = [line for line in crop_info.split("\n") if "crop" in line][-1]
    m = re.search("crop=(\d+:\d+:\d+:\d+)", crop_line)
    if not m:
        print("No crop parameters detected. Exiting.")
        return
    crop_params = m.group(1)
    
    # Use the detected crop parameters to crop the video
    command = [
        "ffmpeg", 
        "-y",
        "-i", video_path, 
        "-vf", f"crop={crop_params}", 
        "-c:a", "copy",
        output_path
    ]
    
    subprocess.run(command)


def compare_to_template(video_path, template_path):
    video = cv2.VideoCapture(video_path)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Check if the template loaded correctly
    if template is None:
        raise Exception(f"Failed to load template image from path: {template_path}")

    template_h, template_w = template.shape

    # Create directory if it doesn't exist
    output_dir = 'CreampuffBOT/temp/vid_imgs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # Clear the directory by deleting all files in it
        for file_name in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    frame_number = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > 0.3934:
            output_path = os.path.join(output_dir, f'frame_{frame_number}.png')
            cv2.imwrite(output_path, frame)
        
        frame_number += 1

    video.release()
    
    
def remove_duplicate_frames(output_dir):
    # Get all saved frame numbers
    frames = [f for f in os.listdir(output_dir) if f.startswith("frame_")]
    frame_numbers = sorted([int(f.split('_')[1].split('.')[0]) for f in frames])

    if not frame_numbers:
        return

    to_keep = []
    start = frame_numbers[0]
    for i in range(1, len(frame_numbers)):
        if frame_numbers[i] - frame_numbers[i-1] > 1:
            end = frame_numbers[i-1]
            middle = (start + end) // 2
            to_keep.append(f'frame_{middle}.png')
            start = frame_numbers[i]

    # Handle the last sequence
    end = frame_numbers[-1]
    middle = (start + end) // 2
    to_keep.append(f'frame_{middle}.png')

    # Remove all frames not in to_keep
    for frame_file in frames:
        if frame_file not in to_keep:
            os.remove(os.path.join(output_dir, frame_file))
    
    
def sliding_window(output_dir):
    frames = sorted([f for f in os.listdir(output_dir) if f.startswith("frame_")])

    to_delete = []
    window_size = 3

    for i in range(0, len(frames) - window_size + 1, window_size):
        window = frames[i: i + window_size]
        
        if i == 0:  # If it's the first window, don't delete the first frame
            to_delete.extend(window[1:-1])
        elif i == len(frames) - window_size:  # If it's the last window, don't delete the last frame
            to_delete.extend(window[:-1])
        else:
            to_delete.extend(window[:-1])


process_video('CreampuffBOT/temp/test_video.mp4', 'CreampuffBOT/temp/test_out.mp4')
print("Done processing video")

#compare_to_template('CreampuffBOT/temp/test_out.mp4', 'CreampuffBOT/src/template.png')
#print("Done comparing to template.. removing duplicate frames")

#remove_duplicate_frames('CreampuffBOT/temp/vid_imgs')
#print("Done removing duplicates .. sliding window across screenshots")

#sliding_window('CreampuffBOT/temp/vid_imgs')
