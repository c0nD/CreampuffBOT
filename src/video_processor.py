import cv2
import image_preprocessor as ipp

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

process_video('CreampuffBOT/temp/test_video.mp4', 'CreampuffBOT/temp/test_out.mp4')
