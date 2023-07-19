import cv2
import image_preprocessor as ipp
import os

def process_video(video_path, output_path):
    video = cv2.VideoCapture(video_path)

    # codec and videowriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (2270, 1080))

    # Find the crop region from the first frame
    ret, frame = video.read()
    if not ret:
        raise Exception("Could not read frame from video")
    frame = ipp.remove_possible_padding(frame)
    frame_height, frame_width = frame.shape[:2]

    while True:
        ret, frame = video.read()
        if not ret:
            break
        # Apply the same crop to each frame
        frame = frame[:frame_height, :frame_width]
        frame = ipp.resize_image_to_aspect_ratio(frame)
        out.write(frame)

    video.release()
    out.release()


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
    
    
    
    


process_video('CreampuffBOT/temp/test_video.mp4', 'CreampuffBOT/temp/test_out.mp4')
print("Done processing video")
compare_to_template('CreampuffBOT/temp/test_out.mp4', 'CreampuffBOT/src/template.png')
