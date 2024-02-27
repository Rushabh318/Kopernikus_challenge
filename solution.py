import glob
import cv2
from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
import numpy as np
from tqdm import tqdm
import os

def data_cleanup(path, threshold, pre_process=False):

    """
    Finds and removes similar-looking images in a folder.

    Args:
    - path: Path to the folder containing images.
    - threshold: Threshold for considering images as similar.
    - pre_process: Set to true to go through the entire the 
            dataset and resize before removing similar images.
            Preferarrbly when going through the dataset for the first time.

    Returns:
    - List of removed image filenames.
    """
    
    # set this to True if all images are to be resized and saved as 640x480 images. 
    if pre_process:
        img_list = glob.glob(path+'/*.png')
        
        for img in img_list:
            try:
                image = cv2.imread(img)
                image = cv2.resize(image, (640, 480))
                cv2.imwrite(img, image)
            except:
                # remove corrupted images, that cannot be opened by cv2
                os.remove(img) 
    
    removed_images = []

    # Load and preprocess the first image for comparison
    img_names = sorted(os.listdir(path))[1:]
    frame_1_path = os.path.join(path, img_names[0])
    frame_1 = cv2.imread(frame_1_path)
    if frame_1.shape[:2] != (640, 480):
        frame_1 = cv2.resize(frame_1, (640, 480))
    gray_1 = preprocess_image_change_detection(frame_1)

    # Iterate over the remaining images in the folder
    for img_name in tqdm(img_names[1:]):
        img_path = os.path.join(path, img_name)
        frame_2 = cv2.imread(img_path)
        if frame_2 is None:
            continue
        if frame_2.shape[:2] != (640, 480):
            frame_2 = cv2.resize(frame_2, (640, 480))
        gray_2 = preprocess_image_change_detection(frame_2)
        score, _, _ = compare_frames_change_detection(gray_1, gray_2, 900)
        
        # If images are too similar, remove the current one
        if score < threshold:
            os.remove(img_path)
            removed_images.append(img_name)
        # Otherwise, update reference image for the next comparison
        else:
            frame_1 = frame_2
            gray_1 = gray_2

    return removed_images


def main():

    path = "dataset-candidates-ml/dataset/"
    threshold = 10000

    data_cleanup(path, threshold)

if __name__ == "__main__":

    main()
