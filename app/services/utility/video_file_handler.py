import os
import cv2


def store_video_file(video, file_path, codec, fps):
    # https://www.geeksforgeeks.org/saving-a-video-using-opencv/
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    if video.isOpened() == False:
        print("Error reading video file")

    print(height, type(width))
    fourcc = cv2.VideoWriter.fourcc(*codec)
    result = cv2.VideoWriter(file_path, fourcc, fps, (int(width), int(height)))

    while (True):
        ret, frame = video.read()
        if not ret:
            break
        result.write(frame)

    video.release()
    result.release()
    cv2.destroyAllWindows()

def delete_video_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The video file does not exist")

def retrieve_video_file(file_path):
    return open(file_path, 'rb')
