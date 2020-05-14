import os
import numpy
import cv2
from PIL import Image


def generate_video():
    os.chdir("C:\\Users\\Daria\\PycharmProjects\\Lab1MathStat\\pictures")
    image_folder = '.'  # убедитесь, что используете вашу папку
    video_name = 'projections_in_area.avi'
    os.chdir("C:\\Users\\Daria\\PycharmProjects\\Lab1MathStat\\pictures")
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    print(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 25, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()  # выпуск сгенерированного видео
