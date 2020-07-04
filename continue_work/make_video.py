import os
import cv2


def generate_video(dir, video_name):
    os.chdir(dir)  # folder for full interval
    image_folder = '.'
    os.chdir(dir)
    images = [[img, os.path.getctime(img)] for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    # sorting for get order of creating
    images = sorted(images, key=lambda img: img[1])
    frame = cv2.imread(os.path.join(image_folder, images[0][0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 1, (width, height))  # 1 - frames per second, 0 - not for change!
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image[0])))
    cv2.destroyAllWindows()
    video.release()
