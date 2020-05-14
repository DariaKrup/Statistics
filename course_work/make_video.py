import os
import cv2


def generate_video():
    os.chdir("C:\\Users\\Daria\\PycharmProjects\\Lab1MathStat\\pictures_full")  # folder for full interval
    image_folder = '.'
    video_name = 'projections_in_area_full.avi'
    os.chdir("C:\\Users\\Daria\\PycharmProjects\\Lab1MathStat\\pictures_full")
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    print(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 25, (width, height))  # 25 - frames per second 
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()
